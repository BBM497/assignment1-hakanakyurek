"""
This script consists of dictionaries of short forms in english.
Documents should be lower cased beforehand.
"""

from itertools import chain
from collections import OrderedDict

# short_not = '[(am)(are)(is)(do)(was)(were)(does)(have)(must)(had)(can)(should)(could)(will)(would)] not'

short_not = {'is not ': 'isn\'t ',
             'are not ': 'aren\'t ',
             'do not ': 'don\'t ',
             'did not ': 'didn\'t ',
             'was not ': 'wasn\'t ',
             'were not ': 'weren\'t ',
             'does not ': 'doesn\'t ',
             'have not ': 'haven\'t ',
             'has not ': 'hasn\'t ',
             'had not ': 'hadn\'t ',
             'must not ': 'musn\'t ',
             'should not ': 'shouldn\'t ',
             'can not ': 'can\'t ',
             'could not ': 'couldn\'t ',
             'will not ': 'won\'t ',
             'would not ': 'wouldn\'t ',
             }


short_to_be = {'i am ': 'i\'m ',
               'he is ': 'he\'s ',
               'she is ': 'she\'s ',
               'it is ': 'it\'s ',
               'you are ': 'you\'re ',
               'we are ': 'we\'re ',
               'they are ': 'they\'re ',
                }

short_have = {'i have ': 'i\'ve ',
              'you have ': 'you\'ve ',
              'she has ': 'she\'s ',
              'he has ': 'he\'s ',
              'it has ': 'it\'s ',
              'we have ': 'we\'ve ',
              'they have ': 'they\'ve ',
              }

short_will = {'i will ': 'i\'ll ',
              'he will ': 'he\'ll ',
              'she will ': 'she\'ll ',
              'you will ': 'you\'ll ',
              'it will ': 'it\'ll ',
              'we will ': 'we\'ll ',
              'they will ': 'they\'ll ',
              'i would ': 'i\'d ',
              'you would ': 'you\'d ',
              'she would ': 'she\'d ',
              'he would ': 'he\'d ',
              'it would ': 'it\'d ',
              'we would ': 'we\'d ',
              'they would ': 'they\'d ',
              }

short_all = OrderedDict(chain(short_not.items(), short_have.items(), short_to_be.items(), short_will.items()))
