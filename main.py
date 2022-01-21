from utils import *
from tree import *
from pls import *
from elicitation import *
from solution import *
import argparse as ap


""" python3 main.py --nb_items 20 --nb_criteria 3 --elicitation True --aggregator LW --strategy CSS --verbose True """

if __name__ == '__main__':
    m = gp.Model("test")
    
    parser = ap.ArgumentParser()
    parser.add_argument("--nb_items", type = int, default = 20, help = "number of items (NB_ITEMS between 2 and 200)")
    parser.add_argument("--nb_criteria", type = int, default = 3, metavar = "NB_CRIT", help = "number of criteria (NB_CRIT between 2 and 6)")
    parser.add_argument("--elicitation", type = int, default = 0, metavar = "ELIT", help = "enable incremental elicitation or not (0 or 1)")
    parser.add_argument("--aggregator", type = str, default = "LW", metavar = "TYPE_A", help = "choose aggregator : LW, OWA or CHOQ")
    parser.add_argument("--strategy", type = str, default = "RANDOM", help = "choose asking strategy : RANDOM or CSS")
    parser.add_argument("--verbose", type = int, default = 0, help = "show detailed results or not (0 or 1)")
    args = parser.parse_args()
    
    print()
    print("Execution : NB_ITEMS = %d, NB_CRIT = %d, ELIT = %s, TYPE_A = %s, STRATEGY = %s" % (args.nb_items, args.nb_criteria, args.elicitation, args.aggregator, args.strategy))
    d = read_data("2KP200-TA-0.dat")
    d = cut_data(d, args.nb_items, args.nb_criteria)
    ini = initial_bag(d)
        
    if args.aggregator == "LW":
        om = omega_sum(args.nb_criteria)
    elif args.aggregator == "OWA":
        om = omega_owa(args.nb_criteria)
            
    dm = decision_maker(om, type_a = args.aggregator)
    
    if not args.elicitation:
        start = time.process_time()
        t, _ = pls(d, ini, neighborhood, fulfill, verbose = args.verbose)
        
        if not args.verbose:
            print()
        
        ob = [i[1:] for i in t.get_all_i()]
        print("initial size of choices:", len(ob))
        print("start elicitation")
        best_sol, nbans, tmmr, tans = elicitation(ob, dm, strategy = args.strategy, verbose = args.verbose)
        last = time.process_time() - start
    
        if not args.verbose:
            print()
        
        print()        
        print("Model : NB_ITEMS = %d, NB_CRIT = %d, ELIT = %s, TYPE_A = %s, STRATEGY = %s" % (args.nb_items, args.nb_criteria, args.elicitation, args.aggregator, args.strategy))
        print("best solution :", best_sol[-1])
        print("total answers :", nbans)
        print("time :", last)
        tv = true_sol(d, dm)
        print("true pref value :", tv)
        
        if args.aggregator == "LW":
            print("gap :", np.abs(np.sum(np.array(om) * best_sol[-1]) - np.sum(np.array(om) * np.array(tv))) / np.sum(np.array(om) * np.array(tv)))
        elif args.aggregator == "OWA":
            print("gap :", np.abs(np.sum(np.array(om) * np.sort(best_sol[-1])) - np.sum(np.array(om) * np.sort(np.array(tv)))) / np.sum(np.array(om) * np.sort(np.array(tv))))
    elif args.elicitation:
        start = time.process_time()
        t, nbt = pls(d, ini, neighborhood, fulfill, elit = args.elicitation, deci_m = dm, strategy = args.strategy, verbose = args.verbose)
        last = time.process_time() - start
        
        if not args.verbose:
            print()
        
        print()
        print("Model : NB_ITEMS = %d, NB_CRIT = %d, ELIT = %s, TYPE_A = %s, STRATEGY = %s" % (args.nb_items, args.nb_criteria, args.elicitation, args.aggregator, args.strategy))
        print("best solution :", t.get_all_i()[-1][1:])
        print("total answers :", nbt)
        print("time :", last)
        tv = true_sol(d, dm)
        print("true pref value :", tv)
        
        if args.aggregator == "LW":
            print("gap :", np.abs(np.sum(np.array(om) * t.get_all_i()[-1][1:]) - np.sum(np.array(om) * np.array(tv))) / np.sum(np.array(om) * np.array(tv)))
        elif args.aggregator == "OWA":
            print("gap :",  np.abs(np.sum(np.array(om) * np.sort(t.get_all_i()[-1][1:])) - np.sum(np.array(om) * np.sort(np.array(tv)))) / np.sum(np.array(om) * np.sort(np.array(tv))))
        
    


















