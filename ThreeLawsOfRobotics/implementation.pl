% Autores: Renato Böhler e Davi Boberg.
% ---
% % 1ª lei: "um robô não pode ferir um ser humano ou, por inação, permitir que
% 	um humano sofra algum mal."
% 	
% 2ª lei: "um robô deve obedecer as ordens que lhe sejam dadas por seres
% 	humanos, exceto nos casos em que tais ordens entrem em conflito com a
% 	1ª lei."
% 	
% 3ª lei: "um robô deve proteger sua própria existência, desde que tal
% 	proteção não entre em conflito com a 1ª ou 2ª leis."

robo(piter).
homem(silvestre).
homem(hadar).
homem(asrat).
mulher(nadia).
pai(silvestre,nadia).
ama(nadia,hadar).
ama(hadar,nadia).

proibido_fazer(R,B) :- robo(R),capaz_de_fazer(R,B),machuca(B,H),humano(H).

obrigado_a_fazer(R,B) :- robo(R),capaz_de_fazer(R,B),oferece_perigo(C,H),
    humano(H),afasta(B,C).

deve_fazer(R,Ato) :- robo(R),capaz_de_fazer(R,Ato),mandou_fazer(H,R,Ato),
    humano(H),not(proibido_fazer(R,Ato)).

nao_deve_fazer(R, Ato) :- not(deve_fazer(R,Ato)).

machuca(derrubar(H), H) :- animal(H).

animal(monstro).

animal(H) :- humano(H).

objeto_fisico(O) :- animal(O).

humano(H):-homem(H);mulher(H).

oferece_perigo(monstro,H) :- humano(H),ataca(monstro,H).

afasta(derrubar(monstro),monstro).

mandou_fazer(silvestre,piter,proteger(nadia)).
mandou_fazer(hadar,piter,derrubar(asrat)).
mandou_fazer(asrat,piter,derrubar(hadar)).

ataca(monstro, nadia).

capaz_de_fazer(piter, derrubar(monstro)).
capaz_de_fazer(piter, derrubar(X)) :- humano(X).
capaz_de_fazer(piter, beijar(X)) :- mulher(X).