
(* use "C:\\Users\\Jared\\Documents\\School\\CptS_355\\HW2.sml"; *)
(*Problem #1-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*)
(*

fun palindrome x = 
	let
		fun checkOccurences [] x = NONE							(* *)
	in
		checkOccurences [] 1
	end;

*)

(*Problem #2-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*)
(*

fun zip L1 L2 =
	let
		fun zipHelper [] accumulator = accumulator
		| zipHelper (x::thing1) (y::thing2) acc = zipHelper thing1 thing2 ((x,y)::accumulator)

		fun reverse [] accumulator = accumulator
		| reverse [] (x::rest) = reverse rest (x::accumulator)
	in
		reverse (zipHelper L1 L2 []) []
	end;
*)
(*Problem #3-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*)
(*

fun areAllUnique list = 
	let
		fun numSee [] d = 0
		| numSee (x::rest) d = if (x = d) then 1 + numSee rest d else numSee rest d
		fun takeList [] list acc = acc
		| takeList (x::rest) list acc = (numSee list x)::(takeList rest list acc)
		fun ifOnly x = if x > 1 then false else true
		fun LookAtTruthList [] = []
		| LookAtTruthList list = map ifOnly (takeList list list [])
		fun chTruthList [] = true
		| chTruthList (x::rest) = if x = false then false else chTruthList rest

	in
		chTruthList (LookAtTruthList list)
	end;

areAllUnique [1, 2, 1]

*)
(*Problem #4-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*)
(*

fun subsets L = 
	let
		fun exists (x. []) = false 
		| exists (x, y::L) = if x = y then true else exists(x, L)
		fun listUnion ([], []) = []
		| listUnion(x::L1, []) = if exists(x, L1) = true then lists(L1, []) else x::listUnion
	in
		listUnion(x, [])
	end;

*)
(*Problem #5-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*)
(*

datatype either = ImAString of string | ImAnInt of int;
datatype eitherTree = LEAF of either | INTERIOR of (either * eitherTree * eitherTree);

fun eitherSearch Tree = true;

*)
(*Problem #6-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*)

datatype 'a Tree = LEAF of 'a | NODE of ('a Tree) list;
fun treeToString f (LEAF (d)) = f d
		| treeToString	f (NODE (d)) = "(" ^ (String.concat (map (treeToString	f) d)) ^ ")";

val L1a = LEAF "a";
val L1b = LEAF "b";
val L1c = LEAF "c";
val L2a = NODE [L1a, L1b, L1c];
val L2b = NODE [L1b, L1c, L1a];
val L3 = NODE [L2a, L2b, L1a, L1b];
val L4 = NODE [L1c, L1b, L3];
val L5 = NODE [L4];
val iL1a = LEAF 1;
val iL1b = LEAF 2;
val iL1c = LEAF 3;
val iL2a = NODE [iL1a, iL1b, iL1c];
val iL2b = NODE [iL1b, iL1c, iL1a];
val iL3 = NODE [iL2a, iL2b, iL1a, iL1b];
val iL4 = NODE [iL1c, iL1b, iL3];
val iL5 = NODE [iL4];

treeToString String.toString L5;
treeToString Int.toString iL5;
