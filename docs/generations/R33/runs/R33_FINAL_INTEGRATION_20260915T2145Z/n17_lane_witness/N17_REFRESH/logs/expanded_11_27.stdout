"""Synthetic verifier checks, never scientific evidence or model fitting."""
import unittest
from e51ai_verify import check_continuity, check_fit, checkpoint_hash, summarize


def cohort():
    return [[1,1,1,int(i<420),1,0,0,1] for i in range(540)]


class VerifierTests(unittest.TestCase):
    def test_exact_accounting(self):
        self.assertEqual(summarize(cohort()), [540,420,120,540,0,0,540,0,0,0,0,540,0,0])

    def test_pointwise_loss_not_hidden_by_sum(self):
        rows=cohort(); rows[0]=[0,1,1,1,0,0,1,1]
        result=summarize(rows)
        self.assertEqual((result[0],result[4],result[7],result[9]), (539,1,1,1))

    def test_missing_episode(self):
        with self.assertRaises(ValueError): summarize(cohort()[:-1])

    def test_bad_t0(self):
        rows=cohort(); rows[0][5]=1
        with self.assertRaises(ValueError): summarize(rows)

    def test_bad_population(self):
        rows=cohort(); rows[0][3]=0
        with self.assertRaises(ValueError): summarize(rows)

    def test_bad_outcome_domain(self):
        rows=cohort(); rows[0][0]=2
        with self.assertRaises(ValueError): summarize(rows)

    def test_fit_identity_and_strict_loss(self):
        check_fit([1,100,99,1]); check_fit([0,99,99,1])
        for bad in ([1,100,101,1],[1,100,99,0],[-1,100,99,1]):
            with self.assertRaises(ValueError): check_fit(bad)

    def test_continuity(self):
        check_continuity(11,22,[11,22])
        with self.assertRaises(ValueError): check_continuity(11,22,[0,22])

    def test_hash_negative_values(self):
        self.assertEqual(checkpoint_hash([0]), (9101*1000003)%2147483629)
        self.assertNotEqual(checkpoint_hash([1,-1]), checkpoint_hash([-1,1]))


if __name__ == "__main__":
    unittest.main()
