# Hand-written paraphrase table — redteam methodology crew, 2026-09-21.
# No RNG, no LLM: every probe below was authored by the redteam analyst.
# Format: (fact_id, family, entity, mild, adversarial)
# MILD: generator's own content vocabulary, syntax the generator never produced.
# ADVERSARIAL: same meaning, content words disjoint from train/test vocabulary
#   wherever a human synonym exists (entity referent kept, as a human needs it).
PARAPHRASES = [
 # ---- alpha-pos (train key ~ {X, alphabet, position}) ----
 (0,  "alpha-pos", "A", "A's alphabet position \u2014 which is it?", "Where does A fall in ABC order?"),
 (5,  "alpha-pos", "F", "F's alphabet position \u2014 which is it?", "Where does F fall in ABC order?"),
 (8,  "alpha-pos", "I", "I's alphabet position \u2014 which is it?", "Where does I fall in ABC order?"),
 (12, "alpha-pos", "M", "M's alphabet position \u2014 which is it?", "Where does M fall in ABC order?"),
 (17, "alpha-pos", "R", "R's alphabet position \u2014 which is it?", "Where does R fall in ABC order?"),
 (21, "alpha-pos", "V", "V's alphabet position \u2014 which is it?", "Where does V fall in ABC order?"),
 (25, "alpha-pos", "Z", "Z's alphabet position \u2014 which is it?", "Where does Z fall in ABC order?"),
 (31, "alpha-pos", "F", "Of F, the alphabet position is what?", "In ABC order, F sits at which spot?"),
 (35, "alpha-pos", "J", "Of J, the alphabet position is what?", "In ABC order, J sits at which spot?"),
 (40, "alpha-pos", "O", "Of O, the alphabet position is what?", "In ABC order, O sits at which spot?"),
 (44, "alpha-pos", "S", "Of S, the alphabet position is what?", "In ABC order, S sits at which spot?"),
 (47, "alpha-pos", "V", "Of V, the alphabet position is what?", "In ABC order, V sits at which spot?"),
 # ---- letter-count (train key ~ {word, X, letter, count}) ----
 (48, "letter-count", "a", "Word \"a\": letter count?", "How many characters compose \"a\"?"),
 (52, "letter-count", "seven", "Word \"seven\": letter count?", "How many characters compose \"seven\"?"),
 (56, "letter-count", "afternoon", "Word \"afternoon\": letter count?", "How many characters compose \"afternoon\"?"),
 (60, "letter-count", "extraordinary", "Word \"extraordinary\": letter count?", "How many characters compose \"extraordinary\"?"),
 (64, "letter-count", "misunderstandings", "Word \"misunderstandings\": letter count?", "How many characters compose \"misunderstandings\"?"),
 (68, "letter-count", "incomprehensibilities", "Word \"incomprehensibilities\": letter count?", "How many characters compose \"incomprehensibilities\"?"),
 (72, "letter-count", "counterdemonstrations", "Word \"counterdemonstrations\": letter count?", "How many characters compose \"counterdemonstrations\"?"),
 (76, "letter-count", "antidisestablishmentarianism", "Word \"antidisestablishmentarianism\": letter count?", "How many characters compose \"antidisestablishmentarianism\"?"),
 (84, "letter-count", "book", "Word \"book\": letter count?", "How many characters compose \"book\"?"),
 (88, "letter-count", "rhyme", "Word \"rhyme\": letter count?", "How many characters compose \"rhyme\"?"),
 (92, "letter-count", "paragraph", "Word \"paragraph\": letter count?", "How many characters compose \"paragraph\"?"),
 (94, "letter-count", "page", "Word \"page\": letter count?", "How many characters compose \"page\"?"),
 # ---- publication-year (train key ~ {entity, publish, year}) ----
 (96,  "pub-year", "Hamlet", "The publication year \u2014 Hamlet?", "When did Hamlet first see print?"),
 (99,  "pub-year", "The King James Bible", "The publication year \u2014 The King James Bible?", "When did The King James Bible first see print?"),
 (104, "pub-year", "Robinson Crusoe", "The publication year \u2014 Robinson Crusoe?", "When did Robinson Crusoe first see print?"),
 (105, "pub-year", "Gulliver's Travels", "The publication year \u2014 Gulliver's Travels?", "When did Gulliver's Travels first see print?"),
 (110, "pub-year", "The Wealth of Nations", "The publication year \u2014 The Wealth of Nations?", "When did The Wealth of Nations first see print?"),
 (111, "pub-year", "Pride and Prejudice", "The publication year \u2014 Pride and Prejudice?", "When did Pride and Prejudice first see print?"),
 (118, "pub-year", "Moby-Dick", "The publication year \u2014 Moby-Dick?", "When did Moby-Dick first see print?"),
 (121, "pub-year", "Madame Bovary", "The publication year \u2014 Madame Bovary?", "When did Madame Bovary first see print?"),
 (124, "pub-year", "Les Miserables", "The publication year \u2014 Les Miserables?", "When did Les Miserables first see print?"),
 (130, "pub-year", "The Brothers Karamazov", "The publication year \u2014 The Brothers Karamazov?", "When did The Brothers Karamazov first see print?"),
 (136, "pub-year", "The Picture of Dorian Gray", "The publication year \u2014 The Picture of Dorian Gray?", "When did The Picture of Dorian Gray first see print?"),
 (142, "pub-year", "The Call of the Wild", "The publication year \u2014 The Call of the Wild?", "When did The Call of the Wild first see print?"),
 # ---- misc-count ----
 (144, "misc", "English alphabet letters", "English alphabet: how many letters?", "The ABCs comprise how many glyphs?"),
 (147, "misc", "week days", "A week: how many days?", "How many sunrises fill one calendar week?"),
 (151, "misc", "day hours", "A day: how many hours?", "One full spin of the Earth holds how many hours?"),
 (155, "misc", "US Constitution amendments", "US Constitution: how many amendments?", "How many times has America's founding charter been formally changed?"),
 (160, "misc", "golf holes", "Full round of golf: how many holes?", "How many holes does a complete circuit of the links contain?"),
 (200, "misc", "apostles of Jesus", "Apostles of Jesus: how many?", "How large was Christ's inner circle of followers?"),
 (204, "misc", "New Testament Gospels", "New Testament: how many Gospels?", "How many accounts of Christ's life open the Christian canon?"),
 (210, "misc", "Harry Potter books", "Harry Potter: how many books?", "How many volumes chronicle the boy wizard's adventures?"),
 (216, "misc", "days of Christmas", "Days of Christmas in the carol: how many?", "The festive song enumerates how many Yuletide occasions?"),
 (217, "misc", "reindeer minus Rudolph", "Reindeer pulling Santa's sleigh, not counting Rudolph: how many?", "Excluding the red-nosed one, how many antlered helpers draw the sleigh?"),
 (220, "misc", "eggs in a dozen", "Eggs in a dozen: how many?", "How many ova fit in a standard egg carton?"),
 (224, "misc", "MLB teams", "Teams in Major League Baseball: how many?", "How many franchises compete in America's pastime top flight?"),
]
