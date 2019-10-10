# UI Mockups For Different Nodes

## Compound

```
==== Compound::<ID> ====
Name: <Compound Name>

==== Self Edge ====
Resembles (CrC): [0...n<Compound::ID>]

==== Outgoing Edges ====
Treates (CtD): [0...n<Disease::ID>]
Palliates (CpD): [0...n<Disease::ID>]
UpRegulates (CuG): [0...n<Gene::ID>]
DownRegulates (CdG): [0...n<Gene::ID>]
Binds (CbG): [0...n<Gene::ID>]

==== Incoming Edges ====
*NONE*
```

## Disease
```
==== Disease::<ID> ====
Name: <Disease Name>

==== Self Edge ====
Resembles (DrD): [0...n<Disease::ID>]

==== Outgoing Edges ====
Localizes (DlA): [0...n<Anatomy::ID>]
UpRegulates (DuG): [0...n<Gene::ID>]
DownRegulates (DdG): [0...n<Gene::ID>]
Associates (DaG): [0...n<Gene::ID>]

==== Incoming Edges ====
Treated by Compound (CtD): [0...n<Disease::ID>]
Palliated by Compound (CpD): [0...n<Disease::ID>]
```

## Anatomy
```
==== Anatomy::<ID> ====
Name: <Anatomy Name>

==== Self Edge ====
*NONE*

==== Outgoing Edges ====
UpRegulates (AuG): [0...n<Gene::ID>]
DownRegulates (AdG): [0...n<Gene::ID>]
Expresses (AeG): [0...n<Gene::ID>]

==== Incoming Edges ====
Localized by Disease (DlA): [0...n<Anatomy::ID>]
```

## Gene
```
==== Gene::<ID> ====
Name: <Gene Name>

==== Self Edge ====
Regulates (Gr>G): [0...n<Gene::ID>]
Covaries (GcG): [0...n<Gene::ID>]
Interacts (GiG): [0...n<Gene::ID>]

==== Outgoing Edges ====
*NONE*

==== Incoming Compound Edges ====
UpRegulates by Compound (CuG): [0...n<Compound::ID>]
DownRegulates by Compound (CdG): [0...n<Compound::ID>]
Binded by Compound(CbG): [0...n<Compound::ID>]

==== Incoming Disease Edges ====
UpRegulates by Disease (DuG): [0...n<Disease::ID>]
DownRegulates by Disease (DdG): [0...n<Disease::ID>]
Associated by Disease (DaG): [0...n<Disease::ID>]

==== Incoming Anatomy Edges ====
UpRegulates by Anatomy (AuG): [0...n<Anatomy::ID>]
DownRegulates by Anatomy (AdG): [0...n<Anatomy::ID>]
Expressed by Anatomy (AeG): [0...n<Anatomy::ID>]
```