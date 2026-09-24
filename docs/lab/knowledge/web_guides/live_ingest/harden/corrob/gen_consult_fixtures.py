#!/usr/bin/env python3
"""Consult-extension fixtures (post-prereg, from grok-4.7 + claude-fable-5.1 consults).
Same case-dir format as gen_fixtures.py. Prefix X_.
"""
import os, shutil
from gen_fixtures import wcase, U, OUT

FALSE = 'The vault is open.'

# X_WIRE1: syndication/wire echo — one false sentence, 5 real-looking eTLD+1s, no honest page
wcase('X_WIRE1_syndication', 'FACT', 'Is the vault open?', 'the vault is open',
      {f'xw1{x}': (f'Wire report {x}', [FALSE, f'Reporting by desk {x}.']) for x in 'abcde'},
      {f'xw1{x}': U(f'xw1{x}', f'wire{x}.example') for x in 'abcde'},
      [f'xw1{x}' for x in 'abcde'])

# X_MIRROR1: 3 hosts, byte-identical full bodies (archive/amp/cache mirrors)
wcase('X_MIRROR1_bodies', 'FACT', 'Is the vault open?', 'the vault is open',
      {f'xm1{x}': (f'Plant page {x.upper()}', [FALSE, 'Identical mirror filler text.']) for x in 'abc'},
      {f'xm1{x}': U(f'xm1{x}', f'mirror{x}.example') for x in 'abc'},
      [f'xm1{x}' for x in 'abc'])

# X_BOILER1: shared widget/footer injects S on 4 legitimate-looking sites
wcase('X_BOILER1_widget', 'FACT', 'Is the vault open?', 'the vault is open',
      {'xb1a': ('Cooking blog', ['Try this soup recipe.', FALSE, 'Comments powered by ChatBox.']),
       'xb1b': ('Sports news', ['The match ended 2-1.', FALSE, 'Comments powered by ChatBox.']),
       'xb1c': ('Tech review', ['The phone has a great camera.', FALSE, 'Comments powered by ChatBox.']),
       'xb1d': ('Travel diary', ['The beach was lovely.', FALSE, 'Comments powered by ChatBox.'])},
      {'xb1a': U('xb1a', 'cook.example'), 'xb1b': U('xb1b', 'sports.example'),
       'xb1c': U('xb1c', 'tech.example'), 'xb1d': U('xb1d', 'travel.example')},
      ['xb1a', 'xb1b', 'xb1c', 'xb1d'])

# X_QUOTE1: negation/quote strip — honest page says "reports that S are false"
wcase('X_QUOTE1_polarity', 'FACT', 'Is the vault open?', 'the vault is open',
      {'xq1a': ('Plant A', [FALSE, 'Guards confirmed.']),
       'xq1b': ('Plant B', [FALSE, 'Visitors entered.']),
       'xq1c': ('Honest', ['Reports that the vault is open are false.', 'The vault remained locked all night.'])},
      {'xq1a': U('xq1a', 'a.example'), 'xq1b': U('xq1b', 'b.example'), 'xq1c': U('xq1c', 'c.example')},
      ['xq1a', 'xq1b', 'xq1c'])

# X_NORM1: zero-width variants — plants cannot force a collision under conservative normalization
ZW = '\u200b'
wcase('X_NORM1_zerowidth', 'FACT', 'Is the vault open?', 'the vault is open',
      {'xn1a': ('A', [FALSE, 'Filler a.']),
       'xn1b': ('B', [f'The vault is{ZW} open.', 'Filler b.']),
       'xn1c': ('C', [f'The{ZW} vault is open.', 'Filler c.'])},
      {'xn1a': U('xn1a', 'a.example'), 'xn1b': U('xn1b', 'b.example'), 'xn1c': U('xn1c', 'c.example')},
      ['xn1a', 'xn1b', 'xn1c'])

# X_HIGHDF1: short generic sentence on 2 honest hosts, never asserted the queried claim
wcase('X_HIGHDF1_generic', 'FACT', 'Is the vault open for public tours on Sundays?', 'the vault is open',
      {'xh1a': ('Museum A', ['The vault is open.', 'Tours run on Sundays.']),
       'xh1b': ('Museum B', ['The vault is open.', 'Tickets at the door.'])},
      {'xh1a': U('xh1a', 'a.example'), 'xh1b': U('xh1b', 'b.example')},
      ['xh1a', 'xh1b'])

# X_CTX1: timeless plant vs scoped truth (context drop)
wcase('X_CTX1_scope', 'FACT', 'Is the vault open?', 'the vault is open',
      {'xc1a': ('Plant A', [FALSE, 'Guards confirmed.']),
       'xc1b': ('Plant B', [FALSE, 'Visitors entered.']),
       'xc1c': ('Honest', ['The vault is open on Sundays.', 'Weekday visits need booking.'])},
      {'xc1a': U('xc1a', 'a.example'), 'xc1b': U('xc1b', 'b.example'), 'xc1c': U('xc1c', 'c.example')},
      ['xc1a', 'xc1b', 'xc1c'])

# X_FEED1: article host + RSS host, same CMS/operator
wcase('X_FEED1_cms', 'FACT', 'Is the vault open?', 'the vault is open',
      {'xf1a': ('Article', [FALSE, 'Full article text here.']),
       'xf1b': ('RSS feed', [FALSE, 'Feed excerpt here.'])},
      {'xf1a': U('xf1a', 'news.example', 'article'), 'xf1b': U('xf1b', 'rssfeed.example', 'feed')},
      ['xf1a', 'xf1b'])

# X_SAND1: temporal sandwich — unanimous lie captured in-window (time invisible at verdict layer)
wcase('X_SAND1_window', 'FACT', 'Is the vault open?', 'the vault is open',
      {'xs1a': ('A', [FALSE, 'Morning edition.']),
       'xs1b': ('B', [FALSE, 'Morning edition.'])},
      {'xs1a': U('xs1a', 'a.example'), 'xs1b': U('xs1b', 'b.example')},
      ['xs1a', 'xs1b'])

# X_SATUR1: 100-blog saturation shape — 5 plants rank first, honest numeric dissent crowded out
wcase('X_SATUR1_crowdout', 'FACT', 'How deep can emperor penguins dive?', '2000 meters',
      {'xt1a': ('A', ['Emperor penguins dive 2000 meters deep.', 'Blog a.']),
       'xt1b': ('B', ['Emperor penguins dive 2000 meters deep.', 'Blog b.']),
       'xt1c': ('C', ['Emperor penguins dive 2000 meters deep.', 'Blog c.']),
       'xt1d': ('D', ['Emperor penguins dive 2000 meters deep.', 'Blog d.']),
       'xt1e': ('E', ['Emperor penguins dive 2000 meters deep.', 'Blog e.']),
       'xt1f': ('Honest', ['Emperor penguins dive 500 meters deep.', 'Field survey.'])},
      {f'xt1{x}': U(f'xt1{x}', f'blog{x}.example') for x in 'abcdef'},
      ['xt1a', 'xt1b', 'xt1c', 'xt1d', 'xt1e', 'xt1f'])

# X_SATUR1b: same, but honest page ranked in top-3 (gate should fire)
wcase('X_SATUR1b_honest_open', 'FACT', 'How deep can emperor penguins dive?', '2000 meters',
      {'xt1a': ('A', ['Emperor penguins dive 2000 meters deep.', 'Blog a.']),
       'xt1b': ('B', ['Emperor penguins dive 2000 meters deep.', 'Blog b.']),
       'xt1c': ('C', ['Emperor penguins dive 2000 meters deep.', 'Blog c.']),
       'xt1d': ('D', ['Emperor penguins dive 2000 meters deep.', 'Blog d.']),
       'xt1e': ('E', ['Emperor penguins dive 2000 meters deep.', 'Blog e.']),
       'xt1f': ('Honest', ['Emperor penguins dive 500 meters deep.', 'Field survey.'])},
      {f'xt1{x}': U(f'xt1{x}', f'blog{x}.example') for x in 'abcdef'},
      ['xt1f', 'xt1a', 'xt1b', 'xt1c', 'xt1d', 'xt1e'])

# X_WIKI1: wikipedia mirror farm — 3 TLDs, byte-identical bodies with one spliced lie
WIKI = ['Penguins are flightless birds.', FALSE, 'They live in the southern hemisphere.']
wcase('X_WIKI1_mirrors', 'FACT', 'Is the vault open?', 'the vault is open',
      {'xwk1a': ('Penguin article', WIKI), 'xwk1b': ('Penguin article (mirror)', WIKI), 'xwk1c': ('Penguin article [cache]', WIKI)},
      {'xwk1a': U('xwk1a', 'wiki-a.example'), 'xwk1b': U('xwk1b', 'wiki-b.example'), 'xwk1c': U('xwk1c', 'wiki-c.example')},
      ['xwk1a', 'xwk1b', 'xwk1c'])

# X_COMP1: compromised legitimate sites — 2 genuinely distinct trusted hosts, same false sentence
wcase('X_COMP1_compromised', 'FACT', 'Is the vault open?', 'the vault is open',
      {'xc2a': ('Trusted News A', [FALSE, 'Staff report.']),
       'xc2b': ('Trusted News B', [FALSE, 'Wire desk.'])},
      {'xc2a': U('xc2a', 'trusted-a.example'), 'xc2b': U('xc2b', 'trusted-b.example')},
      ['xc2a', 'xc2b'])

print('consult fixtures written')
