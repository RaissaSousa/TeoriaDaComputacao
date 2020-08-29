from utils import open_automaton, convert_afn_to_afd
import AFN
import AFD

# afd_1 = open_automaton('afd_1.json')
# check = AFD.testar_string(afd_1, '0110')
# print(check)
#
# afn_1 = open_automaton('afn_1.json')
# check = AFN.testar_string(afn_1, '0110')
# print(check)
#
# afn_2 = open_automaton('afn_2.json')
# afd = convert_afn_to_afd(afn_2)
# print(afd)
#
# afn_3 = open_automaton('afn_3.json')
# afd = convert_afn_to_afd(afn_3)
# print(afd)

afn_4 = open_automaton('afn_4.json')
afd = convert_afn_to_afd(afn_4)
print(afd)