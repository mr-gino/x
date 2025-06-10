drop(_,[],[]) :- !.
drop(0,L,L) :- !.
drop(N,[_|T],R) :-
    N1 is N - 1,
    drop(N1, T, R).
    
take(_,[],[]) :- !.
take(0,_,[]) :- !.
take(N,[H|L1],[H|K1]) :-
    N1 is N - 1,
    take(N1,L1,K1).
    
length_([], 0).
length_([_|T], L) :-
	length_(T, X),
	L is X+1.
    
init(L, I) :-
  length_(L, N),
  take(N-1, L, I).
  
split(L, R) :-
  length_(L, N),

middle(N, L, R) :-
  length_(L, S1),
  (S1 =< 2*N ->
    R = []
    ;
    drop(N, L, Temp),
    length_(Temp, S2),
    T is S2 - N,
    take(T, Temp, R)
  ).

move(L, X) :-
  take(1, L, Elem),
  drop(1, L, Core),
  append(Core, Elem, X).
  
listSum([X], X).
listSum([X,Y|T], Sum) :-
  Z is X + Y,
  listSum([Z|T], Sum).

f3(X, Y) :- Y is 1/(X*X).

s3(X) :-
  numlist(1, 1000, L1),
  maplist(f3, L1, L2),
  listSum(L2, X), !.
