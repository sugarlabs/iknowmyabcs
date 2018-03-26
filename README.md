# Activities/IKnowMyABCs - Sugar Labs

## About I Know My ABCs

![IKnowMyABCsicon.png](docs/IKnowMyABCsicon.png "IKnowMyABCsicon.png")

I Know My ABCs is an activity for introducing the Spanish alphabet. It displays letters and images and associated sound files, such as 'A as in ave'. There are four modes:

1. Click on the letter to hear its name
2. Click on the picture to hear the name of the first letter in the word represented by the picture
3. Hear a letter name, then click on the corresponding letter
4. Hear a letter name, then click on the corresponding picture

(Also see [AEIOU](https://github.com/sugarlabs/AEIOU), [I Can Read](https://github.com/sugarlabs/i-can-read-activity), and [Letter Match](https://github.com/sugarlabs/lettermatch))

## Where to get I Know My ABCs

The I Know My ABCs activity is available for download from the [Sugar Activity Library](http://activities.sugarlabs.org) : [I Know My ABCs](http://activities.sugarlabs.org/en-US/sugar/addon/4625)

The source code is available on [GitHub](https://github.com/sugarlabs/iknowmyabcs).

## Using I Know My ABCs

| ![](docs/180px-IKnowMyABCs.png "180px-IKnowMyABCs.png") | ![](docs/180px-IKnowMyABCs.png "180px-IKnowMyABCs.png") |
|---|---|
| Letter game | Picture game |

### Toolbars

![IKnowMyABCsToolbar.png](docs/IKnowMyABCsToolbar.png "IKnowMyABCsToolbar.png")

Activity toolbar
:  Change the activity name; add notes to the Sugar Journal

Letter mode
: Listen to letter names

Picture mode
: Listen to letter names associated with pictures

Find the letter 1
: Hear a letter spoken and then find it

Find the letter 2
: Hear a word spoken and then find the first letter

Stop button
: Exit the activity

## Learning with I Know My ABCs

While far from contructionist, this activity does provide a mechanism for learning the alphabet.

## Modifying I Know My ABCs

As of Version 1, only a Spanish version is included. In order to add other languages, we need:

* Audio recordings of the letter names
* Audio recordings of the picture names
* Perhaps additional pictures, in order ensure there is a picture for each letter of the alphabet

There is a language-specific database file maintained in ./lessons/??/alphabet.csv where ?? is the 2-digit language code. The format of the CSV file is:

|  letter  |  word  |  color (#RRGGBB) |  image file  |  sound file (image)  |  sound file (letter)  |
|---|---|---|---|---|---|
| R  |  (r)atón  |  #F08020  |  raton.png  |  raton.ogg  |  r.ogg  |

## Extending I Know My ABCs

It would, of course, be fun to let the learner add their own pictures and sound recordings.

## Where to report problems

You are welcome to leave comments/suggestions on the [sugarlabs/iknowmyabcs/issues](https://github.com/sugarlabs/iknowmyabcs/issues) page.

## Credits

I Know My ABCs was written and is maintained by [User:Walter](https://wiki.sugarlabs.org/go/User%3AWalter "User:Walter"). He was inspired in part by the work of Maria Perez, Fundación Zamora Terán
