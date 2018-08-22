/**Facts (at least 100)
*Will include 3 types of factual relationships
*typeof(X,Y) X is type of Y
*partof(X,Y) X is part of Y
*hasprop(X,Y) X has property Y
*/
:-style_check(-discontiguous).

typeof(cat,mammal).
typeof(dog,mammal).
typeof(fish,mammal).
typeof(flower,plant).
typeof(people,mammal).
typeof(animal,organism).
typeof(plant,organism).
hasprop(cat,meow).
hasprop(dog,bark).
hasprop(fish,swim).
hasprop(flower,grow).
hasprop(people,talk).
hasprop(cat,purr).
hasprop(organism,age).
partof(cat,tail).
partof(dog,tail).
partof(fish,tail).
partof(flower,petal).
partof(mammal,hair).
hasprop(organism,reproduction).
partof(animal,eyes).
partof(flower,stem).
partof(plant,roots).
typeof(mammal,animal).
partof(cat,paws).
partof(dog,paws).
hasprop(dog,swim).
hasprop(cat,swim).
hasprop(people,swim).
partof(fish,gills).
partof(cat,ears).
partof(dog,ears).
partof(people,ears).
partof(cat,skin).
partof(dog,skin).
partof(people,skin).
hasprop(mammal,birth).
hasprop(flower,seed).
hasprop(fish,eggs).
partof(mammal,nose).
partof(fish,fins).
partof(people,hands).
partof(people,feet).
partof(people,arms).
partof(people,legs).
partof(cat,arms).
partof(dog,arms).
partof(cat,legs).
partof(dog,legs).
partof(cat,claws).
partof(dog,claws).
typeof(claws,nails).
partof(hands,nails).
hasprop(people,biped).
hasprop(cat,quadruped).
hasprop(dog,quadruped).
hasprop(dog,walk).
hasprop(cat,walk).
hasprop(people,walk).
hasprop(cat,groom).
hasprop(cat,bite).
hasprop(dog,bite).
hasprop(fish,bite).
hasprop(people,bite).
hasprop(animal,breathe).
partof(animal,heart).
hasprop(animal,bleed).
partof(animal,lungs).
hasprop(animal,eat).
hasprop(dog,smell).
hasprop(cat,smell).
hasprop(people,smell).
partof(animal,stomach).
partof(organism,cells).
hasprop(plant,synthesize).
partof(flower,pollen).
partof(flower,pistil).

%%  RULE 1: isa()

isa(X,Y) :- typeof(X,Y).
isa(X,Z) :- typeof(X,Y),isa(Y,Z).

%%  RULE 2: hasproperty()

hasproperty(X,Y) :- hasprop(X,Y).
hasproperty(X,Z) :- typeof(X,Y),hasproperty(Y,Z).

%%  RULE 3: hascomponentpart()

hascomponentpart(X,Y) :- partof(X,Y).
hascomponentpart(X,Z) :- typeof(X,Y),hascomponentpart(Y,Z).
