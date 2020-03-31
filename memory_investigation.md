# Log of some investigation into memory usage

This file contains a log of some interactive pythoning I did to debug memory
usage. Note, I cut a bunch of lines from equipment.csv to make the debugging
faster, but those cuts aren't committed.

## Summary

Most of the memory usage was the unused memory overhead of having a bunch of
tiny `dict`s in the `EquipmentCombination` class. Since there are so many
combinations, even a small overhead adds up.

I reduced memory usage by making EquipmentCombination's implementation a flat
tuple of its arguments and lazily computing member variables. I used @property
so I could be lazy and not modify anything that reads an EquipmentCombination.
This resulted in a ~77% memory reduction.

Even with this, a lot of memory is just `__dict__` for EquipmentCombination.
You could probably further reduce memory overhead by replacing
`List<EquipmentCombination>` with a single `EquipmentCombinationList` class
that just keeps a list of tuples internally and lazily computes the
EquipmentCombination. I think this would work since `tuple` is special in
Python and doesn't need the `__dict__` overhead, but you could avoid `tuple`
overhead by keeping 6 lists in the top-level `EquipmentCombination` (i.e.,
vectorizing the EquipmentCombination)

## Before changing equipment_combination.py

```
$ python3 -i main.py example_data/equipment.csv /dev/null example_data/config.json 
>>> from guppy import hpy; h = hpy().heap()
>>> h
Partition of a set of 1659882 objects. Total size = 327456007 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0 695283  42 231373048  71 231373048  71 dict (no owner)
     1 231660  14 37065600  11 268438648  82 dict of equipment_combination.EquipmentCombination
     2 231829  14 33414096  10 301852744  92 list
     3 231660  14 14826240   5 316678984  97 equipment_combination.EquipmentCombination
     4 232723  14  6516472   2 323195456  99 int
     5  10738   1   955031   0 324150487  99 str
     6   9409   1   766088   0 324916575  99 tuple
     7   2452   0   354664   0 325271239  99 types.CodeType
     8    459   0   354360   0 325625599  99 type
     9   4865   0   345768   0 325971367 100 bytes
<137 more rows. Type e.g. '_.more' to view.>
>>> h.byrcs 
Partition of a set of 1659882 objects. Total size = 327456263 bytes.
 Index  Count   %     Size   % Cumulative  % Referrers by Kind (class / dict of class)
     0 1158300  70 269230752  82 269230752  82 dict of equipment_combination.EquipmentCombination
     1 231660  14 37065600  11 306296352  94 equipment_combination.EquipmentCombination
     2 232518  14 14878522   5 321174874  98 list
     3   1561   0  2146415   1 323321289  99 dict of module
     4  12136   1   958296   0 324279585  99 types.CodeType
     5   4415   0   515553   0 324795138  99 dict of type
     6   4370   0   487782   0 325282920  99 function
     7   1486   0   354104   0 325637024  99 type
     8   4745   0   327670   0 325964694 100 tuple
     9    615   0   160927   0 326125621 100 function, tuple
<447 more rows. Type e.g. '_.more' to view.>
>>> t = h.byrcs[0]
>>> t 
Partition of a set of 1158300 objects. Total size = 269230752 bytes.
 Index  Count   %     Size   % Cumulative  % Referrers by Kind (class / dict of class)
     0 1158300 100 269230752 100 269230752 100 dict of equipment_combination.EquipmentCombination
>>> t.bytype 
Partition of a set of 1158300 objects. Total size = 269230752 bytes.
 Index  Count   %     Size   % Cumulative  % Type
     0 694980  60 231238512  86 231238512  86 dict
     1 231660  20 31505760  12 262744272  98 list
     2 231660  20  6486480   2 269230752 100 int
>>> t.byvia 
Partition of a set of 1158300 objects. Total size = 269230752 bytes.
 Index  Count   %     Size   % Cumulative  % Referred Via:
     0 231660  20 87104160  32  87104160  32 "['equipment']"
     1 231660  20 86682672  32 173786832  65 "['total_skill_levels']"
     2 231660  20 57451680  21 231238512  86 "['total_decoration_slots_by_level']"
     3 231660  20 31505760  12 262744272  98 "['_armour_pieces']"
     4 231660  20  6486480   2 269230752 100 "['total_defence']"
>>> h.bysize 
Partition of a set of 1659882 objects. Total size = 327456927 bytes.
 Index  Count   %     Size   % Cumulative  % Individual Size
     0 459816  28 172890816  53 172890816  53       376
     1 235724  14 58459552  18 231350368  71       248
     2 231855  14 37096800  11 268447168  82       160
     3 231782  14 31522352  10 299969520  92       136
     4 235764  14 15088896   5 315058416  96        64
     5 232667  14  6514676   2 321573092  98        28
     6      1   0  1880816   1 323453908  99   1880816
     7   4666   0   671904   0 324125812  99       144
     8   3706   0   296480   0 324422292  99        80
     9    237   0   252168   0 324674460  99      1064
<573 more rows. Type e.g. '_.more' to view.>
>>> 
```

# After Changing equipment_combination.py

```
$ python3 -i main.py example_data/equipment.csv /dev/null example_data/config.json 
Creating combinations... Done!                    
Scoring and filtering combinations... Done!                    
Exporting combinations... Done!               

Done!
>>> h
Partition of a set of 733305 objects. Total size = 76763227 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0 231829  32 29707536  39  29707536  39 list
     1 231660  32 27799200  36  57506736  75 dict of equipment_combination.EquipmentCombination
     2 231660  32 14826240  19  72332976  94 equipment_combination.EquipmentCombination
     3  10747   1   955763   1  73288739  95 str
     4   9428   1   767336   1  74056075  96 tuple
     5   2459   0   355672   0  74411747  97 types.CodeType
     6    459   0   354232   0  74765979  97 type
     7   4879   1   346292   0  75112271  98 bytes
     8   2235   0   321840   0  75434111  98 function
     9    459   0   252672   0  75686783  99 dict of type
<137 more rows. Type e.g. '_.more' to view.>
>>> 
```
