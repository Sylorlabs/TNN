"""External packet/oracle format tests; never substitute for native ingestion."""
import copy
import struct
import unittest
import zlib

from r33_validate import ContractError, load_json
from r33_c02 import CONFIG, FIELDS, packet, snapshot, checksummed, parse_output, expected_success, expected_output, schedule_count


class EncodedRecordOracles(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.config=load_json(CONFIG)

    def base(self): return packet(self.config,{"kind":"audio"})

    def test_header_and_binary_payload(self):
        raw,meta,payload=self.base()
        self.assertEqual(raw[:8],b"TNNRAW01");self.assertEqual(len(raw),64+len(payload))
        self.assertEqual(struct.unpack("<12I",raw[8:56]),tuple(meta[k] for k in FIELDS))
        self.assertEqual(struct.unpack("<8h",payload),(0,100,0,-32768,-1,1,32767,256))

    def test_packet_checksum_excludes_only_its_fields(self):
        raw,_,_=self.base();a,b=struct.unpack("<II",raw[56:64])
        self.assertEqual(a+(b<<16),zlib.adler32(raw[:56]+raw[64:]))

    def test_snapshot_carries_exact_record_and_cursor(self):
        raw,meta,_=self.base();snap=snapshot(raw,meta)
        self.assertEqual(snap[40:],raw);self.assertEqual(snap[:8],b"TNNSNP01")
        self.assertEqual(struct.unpack("<6I",snap[8:32]),(7,1,100,1000000,len(raw),1))

    def test_snapshot_checksum_detects_cursor_byte_change(self):
        raw,meta,_=self.base();snap=snapshot(raw,meta);bad=bytearray(snap);bad[16]^=1
        self.assertNotEqual(bytes(bad),checksummed(bytes(bad),32))

    def test_lsb_twin_is_one_byte_different(self):
        a,_,_=self.base();b,_,_=packet(self.config,{"kind":"audio","sample_one":101})
        self.assertEqual([i for i in range(64,len(a)) if a[i]!=b[i]],[66])

    def test_visual_pair_preserves_histogram_changes_coordinates(self):
        _,_,a=packet(self.config,{"kind":"rgb"});_,_,b=packet(self.config,{"kind":"rgb","reverse_pixels":True})
        self.assertEqual(sorted(a),sorted(b));self.assertNotEqual(a,b)

    def test_maximum_and_empty(self):
        raw,m,p=packet(self.config,{"kind":"maximum"})
        self.assertEqual(len(raw),131136);self.assertEqual(m["items"],32768)
        self.assertEqual(p[-2:],b"\x01\0")
        raw,m,p=packet(self.config,{"kind":"empty"})
        self.assertEqual(len(raw),64);self.assertEqual(p,b"");self.assertEqual(m["items"],0)

    def test_generation_does_not_mutate_configuration(self):
        original=copy.deepcopy(self.config);self.base();self.assertEqual(original,self.config)

    def test_schedule_is_48_process_cases(self):
        self.assertEqual(schedule_count(self.config),48)
        self.assertEqual(schedule_count(self.config),self.config["expected_native_cases"])
        ids=[x["id"] for x in self.config["cases"]];self.assertEqual(len(ids),len(set(ids)))

    def test_external_decode_oracle(self):
        _,m,p=self.base();metrics,vectors=expected_success(m,p,1)
        self.assertEqual(metrics["used"],80);self.assertEqual(vectors["decoded"],self.config["audio_samples"])

    def test_output_parser(self):
        self.assertEqual(parse_output("M,status,0\nV,cursor,0,7\n"),({"status":0},{"cursor":[7]}))

    def test_duplicate_metric_rejected(self):
        with self.assertRaises(ContractError):parse_output("M,status,0\nM,status,0\n")

    def test_duplicate_vector_rejected(self):
        with self.assertRaises(ContractError):parse_output("V,cursor,0,7\nV,cursor,0,7\n")

    def test_vector_gap_rejected(self):
        with self.assertRaises(ContractError):parse_output("V,cursor,1,7\n")

    def test_non_integer_rejected(self):
        with self.assertRaises(ContractError):parse_output("M,status,NaN\n")

    def test_i32_overflow_rejected(self):
        with self.assertRaises(ContractError):parse_output("M,status,2147483648\n")

    def test_rejected_continuation_retains_exact_prior_record(self):
        raw,meta,_=self.base();m,v=expected_output(-3,None,b"","continue",(raw,meta))
        self.assertEqual(m["used"],80);self.assertEqual(v["retained_bytes"],list(raw))
        self.assertEqual(v["cursor"],[7,1,100,1000000])
        self.assertEqual(m["changed_destination_bytes"],sum(x!=211 for x in raw))

    def test_alias_success_never_claims_detached_input(self):
        _,meta,payload=self.base();m,_=expected_output(0,meta,payload,"alias_forward")
        self.assertEqual(m["detached"],-1);self.assertEqual(m["retrieval_detached"],1)

    def test_empty_has_no_fabricated_decoded_vector(self):
        _,meta,payload=packet(self.config,{"kind":"empty"});_,v=expected_output(0,meta,payload,"capture")
        self.assertNotIn("decoded",v)

    def test_maximum_rgb_byte_oracle(self):
        raw,meta,payload=packet(self.config,{"kind":"rgb_maximum"})
        self.assertEqual(len(payload),12288);self.assertEqual(meta["items"],4096)
        self.assertEqual(payload,bytes(range(256))*48);self.assertEqual(len(raw),12352)

    def test_overmaximum_source_is_not_clipped_by_fixture(self):
        raw,_,payload=packet(self.config,{"kind":"overmaximum"})
        self.assertEqual(len(raw),131138);self.assertEqual(len(payload),131074)

    def test_continuation_rejections_differ_in_registered_metadata(self):
        base,_,_=self.base()
        for spec in self.config["continuation_controls"]:
            raw,meta,_=packet(self.config,{"kind":"audio",**spec})
            self.assertEqual(raw[64:],base[64:]);self.assertEqual(meta["ordinal"],spec["metadata"]["ordinal"])


if __name__=="__main__":unittest.main(verbosity=2)
