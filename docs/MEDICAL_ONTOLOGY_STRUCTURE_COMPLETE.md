# MEDICAL ONTOLOGY STRUCTURE ⭐⭐⭐
## ULTRA-GRANULAR SPECIFICATION FOR NEUROSURGICAL KNOWLEDGE GRAPH ARCHITECTURE

**PURPOSE**: Comprehensive ontological framework for organizing, relating, and querying all neurosurgical knowledge across anatomical, pathological, imaging, and clinical domains. Enables deep semantic extraction, clinical decision support, and intelligent RAG retrieval.

**SCOPE**: Entity taxonomies, relationship types, attribute schemas, cross-domain mappings, standard ontology integration (SNOMED CT, FMA, RadLex), knowledge graph structure, SPARQL-like query patterns, reasoning rules, temporal relationships, probabilistic relationships.

**CLINICAL INTEGRATION**: Surgical planning queries, differential diagnosis generation, treatment recommendation, prognosis prediction, complication risk assessment, imaging interpretation support.

---

## I. ONTOLOGY DESIGN PRINCIPLES ⭐⭐⭐

### FOUNDATIONAL PRINCIPLES ⭐⭐⭐:

├─ Open World Assumption (OWA):
│   ├─ Definition: Absence of statement does NOT imply falsity (vs closed world)
│   ├─ Rationale: Medical knowledge incomplete, continuously evolving
│   ├─ Example: If "tumor enhances" not stated, doesn't mean tumor doesn't enhance
│   └─ Implications: Use explicit negative assertions when needed ("hasEnhancement: false")
│
├─ Monotonicity:
│   ├─ Definition: Adding new information never invalidates previous conclusions
│   ├─ Implementation: Use non-monotonic reasoning layer separately (default logic, defeasible reasoning)
│   └─ Example: New research changes treatment guidelines → version knowledge, don't delete old
│
├─ Compositional semantics:
│   ├─ Complex entities composed from atomic primitives
│   ├─ Example: "Left MCA M1 segment aneurysm" = Location(Left) ∧ Vessel(MCA_M1) ∧ Pathology(Aneurysm)
│   └─ Enables: Automatic inference, flexible querying, knowledge reuse
│
├─ Separation of concerns:
│   ├─ Terminological knowledge (TBox): Class definitions, relationships (schema)
│   ├─ Assertional knowledge (ABox): Instance data (facts about specific patients/cases)
│   └─ Reasoning: Inference engine applies TBox to ABox (derive new facts)
│
└─ Description Logic (DL) expressivity:
    ├─ SROIQ(D): OWL 2 DL profile (decidable, complete reasoning)
    ├─ Balance: Expressivity vs computational tractability
    └─ Features: Role hierarchies, inverse roles, qualified cardinality restrictions, datatypes

---

### STANDARD ONTOLOGY ALIGNMENT ⭐⭐⭐:

├─ Foundational Model of Anatomy (FMA) ⭐⭐⭐:
│   ├─ Coverage: 75,000+ anatomical entities, 120+ relationship types
│   ├─ Integration approach:
│   │   ├─ Map core anatomical entities: Align with FMA IDs (owl:equivalentClass)
│   │   ├─ Example: StudyBuddy:InternalCapsulePosteriorLimb ≡ FMA:62023
│   │   ├─ Import FMA spatial relationships: part_of, tributary_of, branch_of, regional_part_of
│   │   └─ Extend for neurosurgical specificity: Add surgical landmarks, approach corridors
│   ├─ Advantages: Rigor, interoperability, standardized spatial relationships
│   └─ Limitations: Missing functional relationships, clinical context, pathology

├─ SNOMED CT (Systematized Nomenclature of Medicine Clinical Terms) ⭐⭐⭐:
│   ├─ Coverage: 350,000+ clinical concepts, anatomy + pathology + procedures
│   ├─ Integration approach:
│   │   ├─ Clinical entities: Diseases, procedures, findings aligned to SNOMED CT IDs
│   │   ├─ Example: StudyBuddy:Glioblastoma ≡ SNOMEDCT:393563007
│   │   ├─ Precoordinated vs postcoordinated:
│   │   │   ├─ Precoordinated: Single SNOMED CT code (e.g., "Glioblastoma")
│   │   │   └─ Postcoordinated: Compose from primitives (e.g., "Left frontal lobe glioblastoma" = SNOMED expression)
│   │   └─ Relationship import: finding_site, associated_morphology, causative_agent, has_interpretation
│   ├─ Advantages: Comprehensive clinical coverage, hierarchical relationships (IS-A)
│   └─ Use cases: EHR integration, clinical documentation, billing codes (ICD-10 mapping)

├─ RadLex (Radiology Lexicon) ⭐⭐:
│   ├─ Coverage: 68,000+ radiology terms (imaging findings, anatomy, techniques)
│   ├─ Integration approach:
│   │   ├─ Imaging findings: Align imaging phenotypes to RadLex IDs
│   │   ├─ Example: StudyBuddy:RingEnhancement ≡ RadLex:RID5741
│   │   ├─ Imaging techniques: MRI sequences, CT protocols
│   │   └─ Anatomical localization on imaging: RadLex "image location" relationships
│   ├─ Advantages: Structured radiology reporting, AI training data annotation
│   └─ Use cases: Image annotation, CAD systems, radiomics feature extraction

├─ Gene Ontology (GO) and Human Phenotype Ontology (HPO):
│   ├─ GO: Molecular functions, biological processes, cellular components
│   ├─ HPO: Phenotypic abnormalities, clinical features
│   ├─ Integration: Link genetic mutations (IDH1, EGFR) to molecular pathways (GO) and phenotypes (HPO)
│   └─ Use cases: Precision medicine, molecular subtype classification, targeted therapy matching

└─ National Cancer Institute Thesaurus (NCIt):
    ├─ Coverage: Cancer-specific ontology (tumor types, molecular markers, therapies)
    ├─ Integration: Neuro-oncology concepts, molecular classifications (WHO 2021 CNS tumor updates)
    └─ Use cases: Clinical trial matching, molecular marker reporting

---

## II. ENTITY TAXONOMY (TBOX) ⭐⭐⭐

### TOP-LEVEL ENTITY HIERARCHY ⭐⭐⭐:

```
Entity (owl:Thing)
├─ AnatomicalEntity
│   ├─ AnatomicalStructure
│   │   ├─ NervousSystem
│   │   │   ├─ CentralNervousSystem
│   │   │   │   ├─ Brain
│   │   │   │   │   ├─ Forebrain
│   │   │   │   │   │   ├─ Telencephalon (CerebralHemisphere)
│   │   │   │   │   │   │   ├─ CerebralCortex
│   │   │   │   │   │   │   │   ├─ FrontalLobe
│   │   │   │   │   │   │   │   │   ├─ PrimaryMotorCortex (M1, BA4)
│   │   │   │   │   │   │   │   │   ├─ PremotorCortex (BA6)
│   │   │   │   │   │   │   │   │   ├─ SupplementaryMotorArea (SMA)
│   │   │   │   │   │   │   │   │   ├─ BrocasArea (BA44, BA45)
│   │   │   │   │   │   │   │   │   ├─ DorsolateralPrefrontalCortex (DLPFC, BA9, BA46)
│   │   │   │   │   │   │   │   │   └─ VentromedialPrefrontalCortex (VMPFC, BA10, BA11, BA12)
│   │   │   │   │   │   │   │   ├─ ParietalLobe
│   │   │   │   │   │   │   │   │   ├─ PrimarySomatosensoryCortex (S1, BA3, BA1, BA2)
│   │   │   │   │   │   │   │   │   ├─ SuperiorParietalLobule (BA5, BA7)
│   │   │   │   │   │   │   │   │   └─ InferiorParietalLobule (BA39, BA40)
│   │   │   │   │   │   │   │   ├─ TemporalLobe
│   │   │   │   │   │   │   │   │   ├─ SuperiorTemporalGyrus
│   │   │   │   │   │   │   │   │   │   └─ WernickesArea (BA22_posterior)
│   │   │   │   │   │   │   │   │   ├─ MedialTemporalLobe
│   │   │   │   │   │   │   │   │   │   ├─ Hippocampus
│   │   │   │   │   │   │   │   │   │   │   ├─ HippocampusProper (CA1, CA2, CA3, CA4)
│   │   │   │   │   │   │   │   │   │   │   └─ DentateGyrus
│   │   │   │   │   │   │   │   │   │   ├─ Amygdala
│   │   │   │   │   │   │   │   │   │   └─ EntorhinalCortex
│   │   │   │   │   │   │   │   │   └─ TemporalPole
│   │   │   │   │   │   │   │   └─ OccipitalLobe
│   │   │   │   │   │   │   │       ├─ PrimaryVisualCortex (V1, BA17)
│   │   │   │   │   │   │   │       └─ VisualAssociationCortex (V2, V3, V4, V5/MT)
│   │   │   │   │   │   │   ├─ SubcorticalStructures
│   │   │   │   │   │   │   │   ├─ BasalGanglia
│   │   │   │   │   │   │   │   │   ├─ Striatum
│   │   │   │   │   │   │   │   │   │   ├─ Caudate
│   │   │   │   │   │   │   │   │   │   │   ├─ CaudateHead
│   │   │   │   │   │   │   │   │   │   │   ├─ CaudateBody
│   │   │   │   │   │   │   │   │   │   │   └─ CaudateTail
│   │   │   │   │   │   │   │   │   │   └─ Putamen
│   │   │   │   │   │   │   │   │   ├─ GlobusPallidus
│   │   │   │   │   │   │   │   │   │   ├─ GlobusPallidusExterna (GPe)
│   │   │   │   │   │   │   │   │   │   └─ GlobusPallidusInterna (GPi)
│   │   │   │   │   │   │   │   │   ├─ SubstantiaNigra
│   │   │   │   │   │   │   │   │   │   ├─ SubstantiaNigraCompacta (SNc)
│   │   │   │   │   │   │   │   │   │   └─ SubstantiaNigraReticulata (SNr)
│   │   │   │   │   │   │   │   │   └─ SubthalamicNucleus (STN)
│   │   │   │   │   │   │   │   ├─ Thalamus
│   │   │   │   │   │   │   │   │   ├─ AnteriorThalamicNuclei
│   │   │   │   │   │   │   │   │   ├─ MedialThalamicNuclei
│   │   │   │   │   │   │   │   │   ├─ VentralThalamicNuclei
│   │   │   │   │   │   │   │   │   │   ├─ VentralAnteriorNucleus (VA)
│   │   │   │   │   │   │   │   │   │   ├─ VentralLateralNucleus (VL)
│   │   │   │   │   │   │   │   │   │   ├─ VentralPosteriorLateralNucleus (VPL)
│   │   │   │   │   │   │   │   │   │   ├─ VentralPosteriorMedialNucleus (VPM)
│   │   │   │   │   │   │   │   │   │   └─ VentralIntermediateNucleus (VIM)
│   │   │   │   │   │   │   │   │   └─ LateralThalamicNuclei
│   │   │   │   │   │   │   │   │       ├─ LateralGeniculateNucleus (LGN)
│   │   │   │   │   │   │   │   │       └─ MedialGeniculateNucleus (MGN)
│   │   │   │   │   │   │   │   ├─ Hypothalamus
│   │   │   │   │   │   │   │   └─ InternalCapsule
│   │   │   │   │   │   │   │       ├─ AnteriorLimb
│   │   │   │   │   │   │   │       ├─ Genu
│   │   │   │   │   │   │   │       ├─ PosteriorLimb ⭐⭐⭐
│   │   │   │   │   │   │   │       ├─ Retrolenticular
│   │   │   │   │   │   │   │       └─ Sublenticular
│   │   │   │   │   │   │   └─ WhiteMatter
│   │   │   │   │   │   │       ├─ ProjectionFibers
│   │   │   │   │   │   │       │   ├─ CoronaRadiata
│   │   │   │   │   │   │       │   ├─ CorticospinalTract
│   │   │   │   │   │   │       │   ├─ CorticobulbarTract
│   │   │   │   │   │   │       │   ├─ ThalamocoreticalRadiations
│   │   │   │   │   │   │       │   └─ OpticRadiations
│   │   │   │   │   │   │       │       ├─ MeyersLoop (AnteriorBundle)
│   │   │   │   │   │   │       │       ├─ CentralBundle
│   │   │   │   │   │   │       │       └─ PosteriorBundle (DorsalBundle)
│   │   │   │   │   │   │       ├─ CommissuralFibers
│   │   │   │   │   │   │       │   ├─ CorpusCallosum ⭐⭐⭐
│   │   │   │   │   │   │       │   │   ├─ Rostrum
│   │   │   │   │   │   │       │   │   ├─ Genu
│   │   │   │   │   │   │       │   │   ├─ Body
│   │   │   │   │   │   │       │   │   ├─ Splenium
│   │   │   │   │   │   │       │   │   └─ Tapetum
│   │   │   │   │   │   │       │   ├─ AnteriorCommissure
│   │   │   │   │   │   │       │   └─ PosteriorCommissure
│   │   │   │   │   │   │       └─ AssociationFibers
│   │   │   │   │   │   │           ├─ SuperiorLongitudinalFasciculus (SLF)
│   │   │   │   │   │   │           │   ├─ SLF_I
│   │   │   │   │   │   │           │   ├─ SLF_II
│   │   │   │   │   │   │           │   └─ SLF_III
│   │   │   │   │   │   │           ├─ ArcuateFasciculus ⭐⭐
│   │   │   │   │   │   │           ├─ InferiorLongitudinalFasciculus (ILF)
│   │   │   │   │   │   │           ├─ InferiorFrontoOccipitalFasciculus (IFOF)
│   │   │   │   │   │   │           ├─ UncinateFasciculus
│   │   │   │   │   │   │           └─ CingulumBundle
│   │   │   │   │   │   └─ Diencephalon
│   │   │   │   │   │       ├─ ThirdVentricle
│   │   │   │   │   │       ├─ Thalamus (see above)
│   │   │   │   │   │       ├─ Hypothalamus (see above)
│   │   │   │   │   │       ├─ Epithalamus
│   │   │   │   │   │       │   └─ PinealGland
│   │   │   │   │   │       └─ Subthalamus
│   │   │   │   │   ├─ Midbrain (Mesencephalon)
│   │   │   │   │   │   ├─ Tectum
│   │   │   │   │   │   │   ├─ SuperiorColliculi
│   │   │   │   │   │   │   └─ InferiorColliculi
│   │   │   │   │   │   ├─ Tegmentum
│   │   │   │   │   │   │   ├─ RedNucleus
│   │   │   │   │   │   │   ├─ SubstantiaNigra
│   │   │   │   │   │   │   └─ VentralTegmentalArea (VTA)
│   │   │   │   │   │   ├─ CerebralPeduncles
│   │   │   │   │   │   └─ CerebralAqueduct
│   │   │   │   │   └─ Hindbrain (Rhombencephalon)
│   │   │   │   │       ├─ Pons
│   │   │   │   │       │   ├─ BasisPontis
│   │   │   │   │       │   └─ PontineTegmentum
│   │   │   │   │       ├─ Medulla
│   │   │   │   │       │   ├─ Pyramids
│   │   │   │   │       │   ├─ Olives
│   │   │   │   │       │   └─ PyramidalDecussation
│   │   │   │   │       └─ Cerebellum
│   │   │   │   │           ├─ CerebellarHemispheres
│   │   │   │   │           ├─ Vermis
│   │   │   │   │           ├─ CerebellarPeduncles
│   │   │   │   │           │   ├─ SuperiorCerebellarPeduncle
│   │   │   │   │           │   ├─ MiddleCerebellarPeduncle
│   │   │   │   │           │   └─ InferiorCerebellarPeduncle
│   │   │   │   │           └─ DeepCerebellarNuclei
│   │   │   │   │               ├─ DentateNucleus
│   │   │   │   │               ├─ EmboliformNucleus
│   │   │   │   │               ├─ GloboseNucleus
│   │   │   │   │               └─ FastigialNucleus
│   │   │   │   └─ SpinalCord
│   │   │   │       ├─ CervicalSpinalCord (C1-C8)
│   │   │   │       │   ├─ CervicalEnlargement (C3-T1)
│   │   │   │       │   └─ CervicalSegment [individual segments C1-C8]
│   │   │   │       ├─ ThoracicSpinalCord (T1-T12)
│   │   │   │       ├─ LumbarSpinalCord (L1-L5)
│   │   │   │       │   └─ LumbarEnlargement (T11-L1_vertebral)
│   │   │   │       ├─ SacralSpinalCord (S1-S5)
│   │   │   │       ├─ CoccygealSpinalCord
│   │   │   │       ├─ ConusModullaris
│   │   │   │       ├─ SpinalCordGrayMatter
│   │   │   │       │   ├─ DorsalHorn (RexedLaminae_I_to_VI)
│   │   │   │       │   ├─ IntermediateZone (RexedLaminae_VII)
│   │   │   │       │   ├─ VentralHorn (RexedLaminae_VIII_IX)
│   │   │   │       │   └─ CentralCanal (RexedLaminae_X)
│   │   │   │       └─ SpinalCordWhiteMatter
│   │   │   │           ├─ DorsalFuniculus
│   │   │   │           │   ├─ FasciculusGracilis
│   │   │   │           │   └─ FasciculusCuneatus
│   │   │   │           ├─ LateralFuniculus
│   │   │   │           │   ├─ LateralCorticospinalTract
│   │   │   │           │   ├─ RubrospinalTract
│   │   │   │           │   ├─ LateralSpinothalamiTract
│   │   │   │           │   ├─ DorsalSpinocerebellarTract
│   │   │   │           │   └─ VentralSpinocerebellarTract
│   │   │   │           └─ VentralFuniculus
│   │   │   │               ├─ AnteriorCorticospinalTract
│   │   │   │               └─ VestibulospinalTract
│   │   │   └─ PeripheralNervousSystem
│   │   │       ├─ CranialNerves
│   │   │       │   ├─ OlfactoryNerve (CN_I)
│   │   │       │   ├─ OpticNerve (CN_II)
│   │   │       │   ├─ OculomotorNerve (CN_III)
│   │   │       │   │   ├─ SuperiorDivision
│   │   │       │   │   └─ InferiorDivision
│   │   │       │   ├─ TrochlearNerve (CN_IV)
│   │   │       │   ├─ TrigeminalNerve (CN_V) ⭐⭐
│   │   │       │   │   ├─ OphthalmicDivision (V1)
│   │   │       │   │   │   ├─ FrontalNerve
│   │   │       │   │   │   ├─ LacrimalNerve
│   │   │       │   │   │   └─ NasociliaryNerve
│   │   │       │   │   ├─ MaxillaryDivision (V2)
│   │   │       │   │   │   └─ InfraorbitalNerve
│   │   │       │   │   └─ MandibularDivision (V3)
│   │   │       │   │       ├─ InferiorAlveolarNerve
│   │   │       │   │       ├─ LingualNerve
│   │   │       │   │       └─ AuricularNerve
│   │   │       │   ├─ AbducensNerve (CN_VI)
│   │   │       │   ├─ FacialNerve (CN_VII) ⭐⭐
│   │   │       │   │   ├─ IntracranialSegment
│   │   │       │   │   ├─ MeatealSegment
│   │   │       │   │   ├─ LabyrinthineSegment
│   │   │       │   │   ├─ TympanicSegment
│   │   │       │   │   ├─ MastoidSegment
│   │   │       │   │   ├─ ExtracranialSegment
│   │   │       │   │   └─ Branches
│   │   │       │   │       ├─ GreaterPetrosalNerve
│   │   │       │   │       ├─ NerveToStapedius
│   │   │       │   │       ├─ ChordaTympani
│   │   │       │   │       └─ PeripheralBranches (Temporal, Zygomatic, Buccal, Marginal mandibular, Cervical)
│   │   │       │   ├─ VestibulocochlearNerve (CN_VIII)
│   │   │       │   │   ├─ VestibularNerve
│   │   │       │   │   └─ CochlearNerve
│   │   │       │   ├─ GlossopharyngealNerve (CN_IX)
│   │   │       │   ├─ VagusNerve (CN_X)
│   │   │       │   │   ├─ RecurrentLaryngealNerve
│   │   │       │   │   └─ SuperiorLaryngealNerve
│   │   │       │   ├─ AccessoryNerve (CN_XI)
│   │   │       │   │   ├─ CranialRoot
│   │   │       │   │   └─ SpinalRoot
│   │   │       │   └─ HypoglossalNerve (CN_XII)
│   │   │       └─ SpinalNerves
│   │   │           ├─ CervicalNerves (C1-C8)
│   │   │           │   └─ BrachialPlexus (C5-T1)
│   │   │           │       ├─ Roots (C5, C6, C7, C8, T1)
│   │   │           │       ├─ Trunks (Superior, Middle, Inferior)
│   │   │           │       ├─ Divisions (Anterior, Posterior)
│   │   │           │       ├─ Cords (Lateral, Posterior, Medial)
│   │   │           │       └─ TerminalBranches
│   │   │           │           ├─ MusculocutaneousNerve
│   │   │           │           ├─ MedianNerve
│   │   │           │           ├─ UlnarNerve
│   │   │           │           ├─ RadialNerve
│   │   │           │           └─ AxillaryNerve
│   │   │           ├─ ThoracicNerves (T1-T12)
│   │   │           ├─ LumbarNerves (L1-L5)
│   │   │           │   └─ LumbarPlexus (L1-L4)
│   │   │           │       ├─ FemoralNerve
│   │   │           │       ├─ ObturatorNerve
│   │   │           │       └─ LateralFemoralCutaneousNerve
│   │   │           └─ SacralNerves (S1-S5)
│   │   │               ├─ SacralPlexus (L4-S4)
│   │   │               │   ├─ SciaticNerve ⭐⭐
│   │   │               │   │   ├─ TibialNerve
│   │   │               │   │   └─ CommonPeronealNerve (CommonFibularNerve)
│   │   │               │   ├─ SuperiorGlutealNerve
│   │   │               │   ├─ InferiorGlutealNerve
│   │   │               │   └─ PuddendalNerve
│   │   │               └─ CaudaEquina (nerve roots below conus)
│   │   └─ VascularStructures
│   │       ├─ ArterialSystem
│   │       │   ├─ CircleOfWillis ⭐⭐⭐
│   │       │   │   ├─ AnteriorCirculation
│   │       │   │   │   ├─ InternalCarotidArtery (ICA)
│   │   │   │   │   │   │   ├─ ICA_C1_Cervical
│   │   │   │   │   │   │   ├─ ICA_C2_Petrous
│   │   │   │   │   │   │   ├─ ICA_C3_Lacerum
│   │   │   │   │   │   │   ├─ ICA_C4_Cavernous
│   │   │   │   │   │   │   ├─ ICA_C5_Clinoid
│   │   │   │   │   │   │   ├─ ICA_C6_Ophthalmic
│   │   │   │   │   │   │   └─ ICA_C7_Communicating
│   │       │   │   │   ├─ AnteriorCerebralArtery (ACA)
│   │       │   │   │   │   ├─ ACA_A1 ⭐
│   │       │   │   │   │   ├─ ACA_A2
│   │       │   │   │   │   ├─ ACA_A3
│   │       │   │   │   │   ├─ ACA_A4
│   │       │   │   │   │   └─ ACA_A5
│   │       │   │   │   ├─ AnteriorCommunicatingArtery (AComA) ⭐⭐⭐
│   │       │   │   │   └─ MiddleCerebralArtery (MCA) ⭐⭐⭐
│   │       │   │   │       ├─ MCA_M1 (SphenoidalSegment) ⭐
│   │       │   │   │       ├─ MCA_M2 (InsularSegment)
│   │       │   │   │       ├─ MCA_M3 (OpercularSegment)
│   │       │   │   │       └─ MCA_M4 (CorticalSegment)
│   │       │   │   └─ PosteriorCirculation
│   │       │   │       ├─ VertebralArtery
│   │       │   │       │   ├─ VertebralArtery_V1
│   │       │   │       │   ├─ VertebralArtery_V2
│   │       │   │       │   ├─ VertebralArtery_V3
│   │       │   │       │   └─ VertebralArtery_V4
│   │       │   │       ├─ BasilarArtery ⭐⭐
│   │       │   │       ├─ PosteriorCerebralArtery (PCA)
│   │       │   │       │   ├─ PCA_P1 ⭐
│   │       │   │       │   ├─ PCA_P2
│   │       │   │       │   ├─ PCA_P3
│   │       │   │       │   └─ PCA_P4
│   │       │   │       ├─ PosteriorCommunicatingArtery (PComA) ⭐⭐
│   │       │   │       ├─ SuperiorCerebellarArtery (SCA)
│   │       │   │       ├─ AnteriorInferiorCerebellarArtery (AICA)
│   │       │   │       └─ PosteriorInferiorCerebellarArtery (PICA) ⭐
│   │       │   └─ SpinalArteries
│   │       │       ├─ AnteriorSpinalArtery
│   │       │       ├─ PosteriorSpinalArteries
│   │       │       ├─ ArteryOfAdamkiewicz ⭐
│   │       │       └─ RadicularArteries
│   │       └─ VenousSystem ⭐⭐
│   │           ├─ DuralVenousSinuses
│   │           │   ├─ SuperiorSagittalSinus
│   │           │   ├─ InferiorSagittalSinus
│   │           │   ├─ StraightSinus
│   │           │   ├─ TransverseSinus
│   │           │   ├─ SigmoidSinus
│   │           │   ├─ CavernousSinus ⭐⭐
│   │           │   └─ Torcula (ConfluenceOfSinuses)
│   │           ├─ SuperficialCerebralVeins
│   │           │   ├─ SuperiorCerebralVeins
│   │           │   └─ SuperficialMiddleCerebralVein (VeinOfLabbe)
│   │           └─ DeepCerebralVeins
│   │               ├─ InternalCerebralVeins
│   │               ├─ BasalVeinOfRosenthal
│   │               └─ GreatVeinOfGalen
│   ├─ AnatomicalSpaces
│   │   ├─ VentricularSystem
│   │   │   ├─ LateralVentricles
│   │   │   │   ├─ FrontalHorn
│   │   │   │   ├─ Body
│   │   │   │   ├─ Atrium
│   │   │   │   ├─ OccipitalHorn
│   │   │   │   └─ TemporalHorn
│   │   │   ├─ ThirdVentricle
│   │   │   ├─ CerebralAqueduct (AqueductOfSylvius)
│   │   │   └─ FourthVentricle
│   │   ├─ SubarachnoidCisterns ⭐
│   │   │   ├─ SuprasellarCistern
│   │   │   ├─ InterpeduncularCistern
│   │   │   ├─ AmbientCisterns
│   │   │   ├─ QuadrigeminalCistern
│   │   │   ├─ PrepontinePerontine
│   │   │   └─ CerebromedularyCistern (CisternaMagna)
│   │   └─ PotentialSpaces
│   │       ├─ EpiduralSpace
│   │       ├─ SubduralSpace
│   │       └─ SubarachnoidSpace
│   └─ SupportingStructures
│       ├─ MeningesSkull
│       │   ├─ DuraMater
│       │   │   ├─ FalxCerebri
│   │   │       │   ├─ TentoriumCerebelli
│       │   │   └─ FalxCerebelli
│       │   ├─ ArachnoidMater
│       │   │   └─ ArachnoidGranulations
│       │   └─ PiaMater
│       ├─ Skull
│       │   ├─ Calvarium
│       │   │   ├─ FrontalBone
│       │   │   ├─ ParietalBones
│       │   │   ├─ TemporalBones
│       │   │   └─ OccipitalBone
│       │   └─ SkullBase ⭐⭐
│       │       ├─ AnteriorCranialFossa
│       │       ├─ MiddleCranialFossa
│       │       └─ PosteriorCranialFossa
│       │           └─ Foramina [21+ foramina with contents - see previous spec]
│       └─ VertebralColumn
│           ├─ CervicalVertebrae (C1-C7)
│           │   ├─ Atlas (C1)
│           │   └─ Axis (C2)
│           ├─ ThoracicVertebrae (T1-T12)
│           ├─ LumbarVertebrae (L1-L5) ⭐
│           ├─ Sacrum (S1-S5_fused)
│           └─ Coccyx
│
├─ PathologicalEntity
│   ├─ Neoplasm
│   │   ├─ PrimaryBrainTumor
│   │   │   ├─ Glioma
│   │   │   │   ├─ DiffuseGlioma
│   │   │   │   │   ├─ Astrocytoma
│   │   │   │   │   │   ├─ DiffuseAstrocytoma_IDH_mutant (WHO_Grade_2)
│   │   │   │   │   │   ├─ AnaplasticAstrocytoma_IDH_mutant (WHO_Grade_3)
│   │   │   │   │   │   └─ Glioblastoma_IDH_mutant (WHO_Grade_4)
│   │   │   │   │   ├─ Glioblastoma_IDH_wildtype (WHO_Grade_4) ⭐⭐⭐
│   │   │   │   │   └─ Oligodendroglioma (WHO_Grade_2_or_3) ⭐⭐
│   │   │   │   │       ├─ MolecularFeatures: IDH_mutant + 1p19q_codeleted (REQUIRED)
│   │   │   │   └─ CircumscribedGlioma
│   │   │   │       ├─ PilocyticAstrocytoma (WHO_Grade_1) ⭐
│   │   │   │       └─ PleomorphicXanthoastrocytoma
│   │   │   ├─ Meningioma ⭐⭐⭐
│   │   │   │   ├─ Meningioma_Grade_1 (80-85%)
│   │   │   │   ├─ Meningioma_Grade_2_Atypical (10-15%)
│   │   │   │   └─ Meningioma_Grade_3_Anaplastic (1-3%)
│   │   │   ├─ Medulloblastoma
│   │   │   │   ├─ MolecularSubgroups:
│   │   │   │   │   ├─ WNT_activated (best prognosis)
│   │   │   │   │   ├─ SHH_activated
│   │   │   │   │   ├─ Group_3 (worst prognosis)
│   │   │   │   │   └─ Group_4
│   │   │   ├─ Ependymoma
│   │   │   ├─ PituitaryAdenoma ⭐⭐
│   │   │   │   ├─ FunctioningAdenoma
│   │   │   │   │   ├─ Prolactinoma (40%)
│   │   │   │   │   ├─ GH_secreting (20%, acromegaly)
│   │   │   │   │   ├─ ACTH_secreting (15%, Cushing's disease)
│   │   │   │   │   └─ TSH_secreting (rare)
│   │   │   │   └─ NonFunctioningAdenoma (40%)
│   │   │   └─ Craniopharyngioma
│   │   └─ MetastaticBrainTumor ⭐⭐⭐
│   │       ├─ PrimarySource:
│   │       │   ├─ LungCancer (40-50%) ⭐
│   │       │   ├─ BreastCancer (15-20%)
│   │       │   ├─ Melanoma (10%, highest propensity 40-60%)
│   │       │   ├─ RenalCellCarcinoma (5-10%)
│   │       │   └─ ColorectalCancer (5%)
│   │       └─ NumberOfLesions:
│   │           ├─ SolitaryMetastasis (40-50%)
│   │           └─ MultipleMetastases (50-60%)
│   ├─ VascularMalformation
│   │   ├─ Aneurysm ⭐⭐⭐
│   │   │   ├─ SaccularAneurysm (berry aneurysm)
│   │   │   │   ├─ Location: [maps to arterial anatomy above]
│   │   │   │   ├─ Size: Small (<7mm), Large (7-24mm), Giant (≥25mm)
│   │   │   │   ├─ Morphology: Dome, Neck, AspectRatio, DaughterSac
│   │   │   │   └─ RuptureStatus: Ruptured, Unruptured
│   │   │   ├─ FusiformAneurysm
│   │   │   └─ DissectingAneurysm
│   │   ├─ ArteriovenousMalformation (AVM) ⭐⭐
│   │   │   ├─ Components: Nidus, FeedingArteries, DrainingVeins
│   │   │   └─ SpetzlerMartinGrade: Grade_I to Grade_VI
│   │   ├─ CavernousMalformation ⭐
│   │   │   └─ FamilialCavernousmalformation (CCM1/2/3 genes)
│   │   ├─ DuralArteriovenousFistula (dAVF)
│   │   │   └─ BordenClassification: Type_I, Type_II, Type_III
│   │   └─ DevelopmentalVenousAnomaly (DVA)
│   ├─ CerebrovascularDisease
│   │   ├─ IschemicStroke ⭐⭐⭐
│   │   │   ├─ LargeVesselOcclusion (LVO)
│   │   │   ├─ LacunarInfarct
│   │   │   ├─ CardioembolicStroke
│   │   │   └─ WatershedInfarct
│   │   ├─ IntracranialHemorrhage
│   │   │   ├─ IntraparenchymalHemorrhage (IPH) ⭐⭐
│   │   │   │   ├─ HypertensiveHemorrhage
│   │   │   │   │   └─ Location: BasalGanglia/Putamen (most common), Thalamus, Pons, Cerebellum
│   │   │   │   └─ LobarHemorrhage
│   │   │   ├─ SubarachnoidHemorrhage (SAH) ⭐⭐⭐
│   │   │   │   ├─ AneurysmalSAH
│   │   │   │   └─ PerimesencephalicSAH (non-aneurysmal, benign)
│   │   │   ├─ SubduralHematoma (SDH) ⭐⭐
│   │   │   │   ├─ AcuteSDH (<72h, hyperdense)
│   │   │   │   ├─ SubacuteSDH (3days-3weeks, isodense)
│   │   │   │   └─ ChronicSDH (>3weeks, hypodense)
│   │   │   └─ EpiduralHematoma (EDH) ⭐
│   │   └─ CerebralVenousSinusThrombosis (CVST)
│   ├─ DegenerativeDisease
│   │   ├─ SpinalDegenerativeDisease
│   │   │   ├─ DiscHerniation ⭐⭐⭐
│   │   │   │   ├─ Type: Protrusion, Extrusion, Sequestration
│   │   │   │   ├─ Location: Central, Paracentral, Foraminal, Extraforaminal
│   │   │   │   └─ Level: L4_L5 (45-50%), L5_S1 (40-45%), others
│   │   │   ├─ SpinalStenosis ⭐⭐
│   │   │   │   ├─ CentralCanalStenosis
│   │   │   │   ├─ LateralRecessStenosis
│   │   │   │   └─ ForaminalStenosis
│   │   │   ├─ Spondylolisthesis
│   │   │   └─ Spondylolysis
│   │   └─ NeurodegenerativeDisease
│   │       ├─ ParkinsonsDisease
│   │       ├─ AlzheimersDisease
│   │       └─ HuntingtonsDisease
│   ├─ TraumaticInjury
│   │   ├─ TraumaticBrainInjury (TBI) ⭐⭐⭐
│   │   │   ├─ Severity: Mild (GCS_13-15), Moderate (GCS_9-12), Severe (GCS_≤8)
│   │   │   ├─ PrimaryInjury:
│   │   │   │   ├─ Contusion
│   │   │   │   ├─ DiffuseAxonalInjury (DAI)
│   │   │   │   └─ PenetratingingInjury
│   │   │   └─ SecondaryInjury:
│   │   │       ├─ CerebralEdema
│   │   │       ├─ IntracranalHypertension
│   │   │       └─ Ischemia
│   │   ├─ SpinalCordInjury (SCI) ⭐⭐
│   │   │   ├─ Severity: ASIA_A (complete) to ASIA_E (normal)
│   │   │   ├─ Level: Cervical, Thoracic, Lumbar
│   │   │   └─ Syndromes:
│   │   │       ├─ CentralCordSyndrome
│   │   │       ├─ BrownSequardSyndrome
│   │   │       ├─ AnteriorCordSyndrome
│   │   │       └─ PosteriorCordSyndrome
│   │   └─ SkullFracture
│   │       ├─ LinearFracture
│   │       ├─ DepressedFracture
│   │       └─ BasilarSkullFracture
│   ├─ InfectiousDisease
│   │   ├─ CNS_Infection
│   │   │   ├─ Meningitis
│   │   │   │   ├─ BacterialMeningitis
│   │   │   │   ├─ ViralMeningitis
│   │   │   │   └─ FungalMeningitis
│   │   │   ├─ Encephalitis
│   │   │   └─ BrainAbscess ⭐
│   │   │       └─ Imaging: RingEnhancement + RestrictedDiffusion (distinguishes from tumor)
│   │   └─ SpinalInfection
│   │       ├─ DiscitisOsteomyelitis ⭐⭐
│   │       └─ EpiduralAbscess ⭐
│   ├─ Hydrocephalus ⭐⭐⭐
│   │   ├─ ObstructiveHydrocephalus (NonCommunicating)
│   │   │   └─ ObstructionSite: ForamenOfMonro, AqueductOfSylvius, FourthVentricleOutlets
│   │   ├─ CommunicatingHydrocephalus
│   │   │   ├─ PostHemorrhagicHydrocephalus
│   │   │   ├─ PostInfectiousHydrocephalus
│   │   │   └─ NormalPressureHydrocephalus (NPH) ⭐⭐
│   │   │       └─ HakimTriad: GaitDisturbance, CognitiveImpairment, UrinaryIncontinence
│   │   └─ CongenitalHydrocephalus
│   └─ FunctionalDisorder
│       ├─ EpilepsyEpilepsy ⭐⭐
│       │   ├─ FocalEpilepsy
│       │   │   └─ TemporalLobeEpilepsy (TLE)
│       │   │       └─ MesialTemporalSclerosis
│       │   └─ GeneralizedEpilepsy
│       ├─ MovementDisorder
│       │   ├─ EssentialTremor
│       │   ├─ Dystonia
│       │   └─ ParkinsonsDisease
│       └─ ChronicPain
│           ├─ TrigeminalNeuralgia
│           └─ CentralNeuropathicPain
│
├─ ClinicalFinding
│   ├─ Sign
│   │   ├─ NeurologicalSign
│   │   │   ├─ MotorDeficit
│   │   │   │   ├─ Hemiparesis
│   │   │   │   ├─ Paraparesis
│   │   │   │   ├─ Quadriparesis
│   │   │   │   └─ FootDrop (L5_radiculopathy)
│   │   │   ├─ SensoryDeficit
│   │   │   │   ├─ Hemianesthesia
│   │   │   │   ├─ SaddleAnesthesia (CaudaEquinaSyndrome) ⭐
│   │   │   │   └─ DermatomalSensoryLoss
│   │   │   ├─ ReflexAbnormality
│   │   │   │   ├─ Hyperreflexia (UMN lesion)
│   │   │   │   ├─ Hyporeflexia (LMN lesion)
│   │   │   │   ├─ BabinskiSign (UMN lesion)
│   │   │   │   └─ Clonus
│   │   │   ├─ CranialNervePalsy
│   │   │   │   ├─ CN_III_Palsy
│   │   │   │   │   ├─ PupilInvolving (compressive, e.g., PComA aneurysm) ⭐
│   │   │   │   │   └─ PupilSparing (ischemic, e.g., diabetic)
│   │   │   │   ├─ CN_VII_Palsy (FacialNervePalsy)
│   │   │   │   │   ├─ CentralFacialPalsy (forehead spared, UMN)
│   │   │   │   │   └─ PeripheralFacialPalsy (forehead involved, LMN)
│   │   │   │   └─ [Other CN palsies...]
│   │   │   ├─ GaitAbnormality
│   │   │   │   ├─ AtaxicGait (cerebellar lesion)
│   │   │   │   ├─ HemipareticGait
│   │   │   │   ├─ MagneticGait (NPH) ⭐
│   │   │   │   └─ ParkinsoniGait
│   │   │   ├─ Aphasia
│   │   │   │   ├─ BrocasAphasia (non-fluent, comprehension preserved) ⭐
│   │   │   │   ├─ WernickesAphasia (fluent, comprehension impaired) ⭐
│   │   │   │   ├─ ConductionAphasia (impaired repetition, arcuate fasciculus) ⭐
│   │   │   │   └─ GlobalAphasia
│   │   │   └─ VisualFieldDefect
│   │   │       ├─ BitemporalHemianopia (optic chiasm) ⭐
│   │   │       ├─ HomonymousHemianopia (optic tract, optic radiations, occipital cortex)
│   │   │       └─ Quadrantanopia
│   │   │           ├─ SuperiorQuadrantanopia ("pie in the sky", Meyer's loop) ⭐
│   │   │           └─ InferiorQuadrantanopia
│   │   └─ ImagingFinding ⭐⭐⭐
│   │       ├─ CT_Finding
│   │       │   ├─ Hyperdensity
│   │       │   │   ├─ AcuteHemorrhage (50-90 HU)
│   │       │   │   ├─ Calcification (>100 HU)
│   │       │   │   └─ HyperdenseVesselSign (acute thrombus)
│   │       │   ├─ Hypodensity
│   │       │   │   ├─ Edema
│   │       │   │   ├─ Infarction
│   │       │   │   └─ CSF
│   │       │   └─ MidlineShift (>5mm significant mass effect)
│   │       ├─ MRI_Finding
│   │       │   ├─ T1_Signal
│   │       │   │   ├─ T1_Hyperintense: Fat, SubacuteBlood (methemoglobin), Melanin, Protein
│   │       │   │   └─ T1_Hypointense: CSF, Edema
│   │       │   ├─ T2_Signal
│   │       │   │   ├─ T2_Hyperintense: CSF, Edema, Infarction, Demyelination, Tumor
│   │       │   │   └─ T2_Hypointense: HemoasidemosderinBlood, Calcification
│   │       │   ├─ ContrastEnhancement ⭐⭐
│   │       │   │   ├─ RingEnhancement
│   │       │   │   │   ├─ GBM: Thick irregular ring, nodular
│   │       │   │   │   ├─ Metastasis: Smooth thin ring
│   │       │   │   │   ├─ Abscess: Smooth rim + restricted diffusion ⭐
│   │       │   │   │   └─ SubacuteInfarct: Gyral enhancement
│   │       │   │   ├─ HomogeneousEnhancement
│   │       │   │   │   ├─ Meningioma: Intense enhancement, dural tail ⭐
│   │       │   │   │   └─ Schwannoma: Intense enhancement
│   │       │   │   └─ NoEnhancement
│   │       │   │       └─ LowGradeGlioma: T2/FLAIR hyperintensity, no enhancement
│   │       │   ├─ DWI_RestrictedDiffusion ⭐⭐⭐
│   │       │   │   ├─ AcuteInfarction (cytotoxic edema) ⭐
│   │       │   │   ├─ Abscess (high cellularity)
│   │       │   │   ├─ Epidermoidcyst
│   │       │   │   └─ HypercellularTumor (lymphoma, medulloblastoma)
│   │       │   └─ PerfusionAbnormality
│   │       │       ├─ ElevatedCBV (high-grade glioma, angiogenesis)
│   │       │       └─ DecreasedCBV_CBF (infarct core)
│   │       └─ AngiographicFinding
│   │           ├─ VesselOcclusion (acute stroke, LVO)
│   │           ├─ VesselStenosis (atherosclerosis, vasospasm)
│   │           └─ VascularMalformation (aneurysm, AVM, dAVF)
│   └─ Symptom
│       ├─ Headache
│       │   ├─ ThunderclampHeadache (SAH) ⭐
│       │   ├─ MorningHeadache (↑ ICP, brain tumor)
│       │   └─ PositionalHeadache (CSF leak, low pressure)
│       ├─ Seizure
│       │   ├─ FocalSeizure
│       │   └─ GeneralizedSeizure
│       ├─ VertigoUnbalance
│       ├─ NauseaVomiting (↑ ICP, posterior fossa lesion)
│       └─ CognitiveChange
│           ├─ MemoryImpairment
│           ├─ ExecutiveDysfunction
│           └─ Confusion
│
├─ Intervention (Treatment)
│   ├─ SurgicalProcedure ⭐⭐⭐
│   │   ├─ Craniotomy
│   │   │   ├─ PterionalCraniotomy (AComA, PComA, MCA aneurysms)
│   │   │   ├─ FrontalCraniotomy
│   │   │   ├─ TemporalCraniotomy
│   │   │   ├─ SuboccipitalCraniotomy (posterior fossa)
│   │   │   └─ OrbitozygomonOzygomaticCraniotomy
│   │   ├─ TumorResection
│   │   │   ├─ GrossTotalResection (GTR, >98%) ⭐
│   │   │   ├─ SubtotalResection (STR, 80-98%)
│   │   │   └─ Biopsy (stereotactic needle biopsy)
│   │   ├─ AneurysmTreatment
│   │   │   ├─ MicrosurgicalClipping ⭐⭐
│   │   │   └─ EndovascularCoiling ⭐⭐
│   │   │       └─ Adjuncts: BalloonAssistedCoiling, StentAssistedCoiling, FlowDiversion
│   │   ├─ AVMTreatment
│   │   │   ├─ MicrosurgicalResection
│   │   │   ├─ Embolization (preoperative or standalone)
│   │   │   └─ StereotacticRadiosurgery (SRS)
│   │   ├─ SpineSurgery
│   │   │   ├─ Discectomy
│   │   │   │   ├─ Microdiscectomy ⭐⭐
│   │   │   │   └─ EndoscopicDiscectomy
│   │   │   ├─ Laminectomy (decompression for stenosis) ⭐
│   │   │   ├─ SpinalFusion ⭐
│   │   │   │   └─ Instrumentation: PedicleScrewsRods, InterplayFusion
│   │   │   └─ VertebroplastyKyphoplasty
│   │   ├─ ShuntPlacement
│   │   │   ├─ VentriculoperitonealShunt (VP shunt) ⭐⭐
│   │   │   ├─ VentriculoatrialShunt
│   │   │   └─ LumboperitonealShunt
│   │   ├─ FunctionalNeurosurgery
│   │   │   ├─ DeepBrainStimulation (DBS) ⭐⭐
│   │   │   │   ├─ Target: STN (Parkinson's), GPi, VIM (tremor)
│   │   │   │   └─ Components: Electrode, ExtensionWire, ImplantablePulseGenerator (IPG)
│   │   │   ├─ EpilepsySurgery
│   │   │   │   ├─ AnteriorTemporalLobectomy ⭐
│   │   │   │   ├─ Lesionectomy
│   │   │   │   └─ CorpusCallosotomy
│   │   │   └─ NeuromodulationForPain
│   │   │       ├─ SpinalCordStimulation (SCS)
│   │   │       └─ MotorCortexStimulation
│   │   └─ TraumaSurgery
│   │       ├─ HematomaEvacuation (EDH, SDH)
│   │       ├─ DecompressiveCraniectomy ⭐⭐
│   │       └─ ICP_MonitorPlacement (EVD, intraparenchymal)
│   ├─ RadiationTherapy ⭐⭐⭐
│   │   ├─ ExternalBeamRadiotherapy (EBRT)
│   │   │   ├─ Fractionated: 60 Gy / 30 fractions (GBM standard) ⭐
│   │   │   └─ Hypofractionated: 40 Gy / 15 fractions (elderly GBM)
│   │   ├─ StereotacticRadiosurgery (SRS) ⭐⭐⭐
│   │   │   ├─ GammaKnife
│   │   │   ├─ Linac-based (CyberKnife, TrueBeam)
│   │   │   ├─ Indications: Metastases (1-4 lesions), AVMs, meningiomas, acoustic neuromas
│   │   │   └─ Dose: 12-24 Gy (single fraction), size-dependent
│   │   └─ ProtonTherapy
│   ├─ SystemicTherapy
│   │   ├─ Chemotherapy
│   │   │   ├─ Temozolomide (TMZ) ⭐⭐⭐
│   │   │   │   ├─ Indications: Glioblastoma (Stupp protocol)
│   │   │   │   └─ Dosing: 75 mg/m² (concurrent RT), 150-200 mg/m² days 1-5/28 (adjuvant)
│   │   │   ├─ PCV (Procarbazine, CCNU, Vincristine) ⭐
│   │   │   │   └─ Indications: Oligodendroglioma (1p/19q codeleted)
│   │   │   └─ Bevacizumab ⭐
│   │   │       ├─ Mechanism: Anti-VEGF (angiogenesis inhibitor)
│   │   │       └─ Indications: Recurrent GBM (symptomatic benefit, no OS improvement)
│   │   └─ TargetedTherapy
│   │       ├─ TyrosineKinaseInhibitors
│   │       │   ├─ Osimertinib (EGFR+ NSCLC brain mets) ⭐
│   │       │   └─ Alectinib (ALK+ NSCLC brain mets)
│   │       └─ BRAF_MEK_Inhibitors
│   │           └─ Dabrafenib_Trametinib (BRAF V600E melanoma brain mets)
│   ├─ MedicalManagement
│   │   ├─ AntiepilepticDrugs (AEDs)
│   │   │   ├─ Levetiracetam (Keppra)
│   │   │   ├─ Lacosamide
│   │   │   └─ Lamotrigine
│   │   ├─ Corticosteroids
│   │   │   └─ Dexamethasone (vasogenic edema reduction)
│   │   ├─ OsmoticAgents
│   │   │   ├─ Mannitol (20%, 0.25-1 g/kg)
│   │   │   └─ HypertonicSaline (3%, 23.4%)
│   │   ├─ VasodilatorForVasospasm
│   │   │   └─ Nimodipine (60 mg PO q4h × 21 days, SAH) ⭐⭐⭐
│   │   └─ DopamineAgonist
│   │       └─ Cabergoline (prolactinoma first-line) ⭐
│   └─ SupportiveCare
│       ├─ PhysicalTherapy
│       ├─ OccupationalTherapy
│       ├─ SpeechTherapy
│       └─ PainManagement
│
├─ DiagnosticTest
│   ├─ ImagingModality
│   │   ├─ CT ⭐⭐⭐
│   │   │   ├─ NonContrastCT (NCCT)
│   │   │   ├─ ContrastEnhancedCT (CECT)
│   │   │   ├─ CTAngiography (CTA) ⭐
│   │   │   └─ CTPerfusion (CTP) ⭐
│   │   ├─ MRI ⭐⭐⭐
│   │   │   ├─ StructuralMRI
│   │   │   │   ├─ T1_weighted
│   │   │   │   ├─ T2_weighted
│   │   │   │   ├─ FLAIR
│   │   │   │   ├─ GRE_SWI
│   │   │   │   └─ ContrastEnhancedT1
│   │   │   ├─ FunctionalMRI (fMRI) ⭐
│   │   │   │   └─ Applications: Motor mapping, language mapping
│   │   │   ├─ DiffusionWeightedImaging (DWI) ⭐⭐⭐
│   │   │   │   └─ ADC (Apparent Diffusion Coefficient)
│   │   │   ├─ DiffusionTensorImaging (DTI) ⭐⭐
│   │   │   │   └─ Tractography (white matter mapping)
│   │   │   ├─ PerfusionMRI
│   │   │   │   ├─ DSC (dynamic susceptibility contrast)
│   │   │   │   └─ ASL (arterial spin labeling)
│   │   │   ├─ MRAngiography (MRA) ⭐
│   │   │   ├─ MRVenography (MRV)
│   │   │   └─ MRSpectroscopy (MRS) ⭐
│   │   │       └─ Metabolites: NAA, Choline, Creatine, Lactate
│   │   ├─ DSA (Digital Subtraction Angiography) ⭐⭐
│   │   │   └─ GoldStandard: Aneurysm characterization, AVM angioarchitecture
│   │   └─ NuclearMedicine
│   │       ├─ PET
│   │       │   ├─ FDG_PET
│   │       │   └─ AminoAcid_PET (methionine, FET)
│   │       └─ SPECT
│   ├─ LaboratoryTest
│   │   ├─ MolecularMarker
│   │   │   ├─ IDH_mutation (IDH1, IDH2) ⭐⭐⭐
│   │   │   ├─ 1p19q_codeletion (oligodendroglioma) ⭐⭐⭐
│   │   │   ├─ MGMT_promoter_methylation (GBM prognosis) ⭐⭐⭐
│   │   │   ├─ EGFR_amplification
│   │   │   ├─ TP53_mutation
│   │   │   └─ ATRX_loss
│   │   └─ HormoneLevel
│   │       ├─ Prolactin
│   │       ├─ GH_IGF1
│   │       └─ ACTH_Cortisol
│   └─ ElectrophysiologicalTest
│       ├─ EEG (Electroencephalography)
│       ├─ EMG_NCS (Electromyography, Nerve Conduction Studies)
│       └─ SSEP_MEP (Somatosensory/Motor Evoked Potentials)
│
└─ Outcome
    ├─ ClinicalOutcome
    │   ├─ Survival
    │   │   ├─ OverallSurvival (OS)
    │   │   ├─ ProgressionFreeSurvival (PFS)
    │   │   └─ MedianSurvival
    │   ├─ FunctionalStatus
    │   │   ├─ KarnofskyPerformanceStatus (KPS)
    │   │   ├─ GlasgowOutcomeScale (GOS)
    │   │   │   └─ Extended_GOS (GOSE): Scores 1-8
    │   │   └─ ModifiedRankinScale (mRS): Scores 0-6
    │   └─ QualityOfLife
    │       └─ Measures: SF-36, EORTC QLQ-C30
    ├─ TumorResponse
    │   ├─ CompleteResponse (CR)
    │   ├─ PartialResponse (PR)
    │   ├─ StableDisease (SD)
    │   └─ ProgressiveDisease (PD)
    └─ Complication
        ├─ SurgicalComplication
        │   ├─ Infection (wound, hardware, shunt)
        │   ├─ CSF_Leak
        │   ├─ NeurologicalDeficit (motor, sensory, cognitive)
        │   ├─ Hemorrhage (postoperative)
        │   └─ Seizure
        ├─ RadiationComplication
        │   ├─ RadiationNecrosis
        │   ├─ Neurocognitivedecline
        │   └─ Hypopituitarism
        └─ ChemotherapyComplication
            ├─ Myelosuppression
            ├─ Nausea
            └─ Fatigue
```

---

## III. RELATIONSHIP TYPES (OBJECT PROPERTIES) ⭐⭐⭐

### ANATOMICAL RELATIONSHIPS ⭐⭐⭐:

├─ **part_of** (transitivity: yes, reflexivity: no):
│   ├─ Definition: X part_of Y ≡ X is a constituent component of Y
│   ├─ Domain: AnatomicalEntity
│   ├─ Range: AnatomicalEntity
│   ├─ Examples:
│   │   ├─ Hippocampus part_of MedialTemporalLobe
│   │   ├─ InternalCapsulePosteriorLimb part_of InternalCapsule
│   │   ├─ ACA_A1 part_of AnteriorCerebralArtery
│   │   └─ DorsalHorn part_of SpinalCordGrayMatter
│   ├─ Inference: If A part_of B and B part_of C, then A part_of C (transitivity)
│   └─ FMA alignment: maps to FMA:part_of (FMA:7601)

├─ **regional_part_of**:
│   ├─ Definition: X regional_part_of Y ≡ X is spatially contained within Y (looser than part_of)
│   ├─ Examples:
│   │   ├─ Glioblastoma regional_part_of FrontalLobe (tumor location)
│   │   └─ Aneurysm regional_part_of CircleOfWillis

├─ **tributary_of** (vascular hierarchy):
│   ├─ Definition: X tributary_of Y ≡ X is a vessel branch originating from Y
│   ├─ Inverse: has_tributary
│   ├─ Examples:
│   │   ├─ MCA_M1 tributary_of ICA_C7_Communicating
│   │   ├─ ACA_A1 tributary_of ICA_C7_Communicating
│   │   ├─ PCA_P1 tributary_of BasilarArtery
│   │   └─ SuperiorCerebellarArtery tributary_of BasilarArtery

├─ **continuous_with**:
│   ├─ Definition: X continuous_with Y ≡ X and Y share anatomical continuity (symmetric)
│   ├─ Symmetry: yes
│   ├─ Examples:
│   │   ├─ InternalCapsule continuous_with CoronaRadiata
│   │   ├─ CorticospinalTract continuous_with LateralCorticospinalTract
│   │   └─ ThirdVentricle continuous_with CerebralAqueduct

├─ **adjacent_to** (spatial proximity):
│   ├─ Definition: X adjacent_to Y ≡ X is spatially proximate to Y (symmetric)
│   ├─ Symmetry: yes
│   ├─ Examples:
│   │   ├─ InternalCapsulePosteriorLimb adjacent_to Thalamus
│   │   ├─ CavernousSinus adjacent_to ICA_C4_Cavernous
│   │   └─ OpticChiasm adjacent_to PituitaryGland

├─ **supplies** (arterial supply):
│   ├─ Definition: X supplies Y ≡ X (artery) provides blood supply to Y (anatomical structure)
│   ├─ Domain: ArterialSystem
│   ├─ Range: AnatomicalEntity
│   ├─ Inverse: supplied_by
│   ├─ Examples:
│   │   ├─ MCA_M1 supplies LenticulostriateArteries supplies BasalGanglia
│   │   ├─ ACA supplies MedialFrontalLobe
│   │   ├─ PCA supplies OccipitalLobe
│   │   ├─ PICA supplies LateralMedulla, InferiorCerebellum
│   │   └─ AnteriorSpinalArtery supplies AnteriorTwoThirds_SpinalCord

└─ **drains_into** (venous drainage):
    ├─ Definition: X drains_into Y ≡ X (vein/structure) drains blood into Y (vein/sinus)
    ├─ Examples:
    │   ├─ SuperiorCerebralVeins drains_into SuperiorSagittalSinus
    │   ├─ InternalCerebralVeins drains_into GreatVeinOfGalen
    │   └─ SigmoidSinus drains_into InternalJugularVein

---

### PATHOLOGICAL RELATIONSHIPS ⭐⭐⭐:

├─ **has_location** (pathology-anatomy):
│   ├─ Definition: X has_location Y ≡ Pathological entity X is spatially located in anatomical entity Y
│   ├─ Domain: PathologicalEntity
│   ├─ Range: AnatomicalEntity
│   ├─ Examples:
│   │   ├─ Glioblastoma has_location FrontalLobe
│   │   ├─ Aneurysm has_location AComA
│   │   ├─ DiscHerniation has_location L4_L5_Level
│   │   └─ Meningioma has_location FalxCerebri

├─ **causes** (pathology-clinical finding):
│   ├─ Definition: X causes Y ≡ Pathological entity X produces clinical finding Y
│   ├─ Domain: PathologicalEntity
│   ├─ Range: ClinicalFinding
│   ├─ Examples:
│   │   ├─ Glioblastoma causes Seizure
│   │   ├─ Glioblastoma causes FocalNeurologicalDeficit
│   │   ├─ AneurysmalSAH causes ThunderclampHeadache
│   │   ├─ L5_DiscHerniation causes FootDrop
│   │   ├─ NPH causes MagneticGait
│   │   ├─ PComA_Aneurysm causes CN_III_Palsy_PupilInvolving
│   │   └─ BrocasArea_Lesion causes BrocasAphasia

├─ **associated_with** (pathology-pathology comorbidity):
│   ├─ Definition: X associated_with Y ≡ X and Y co-occur with statistical correlation
│   ├─ Symmetry: yes
│   ├─ Examples:
│   │   ├─ Meningioma associated_with NF2_mutation
│   │   ├─ CavernousMalformation associated_with CCM1_mutation
│   │   ├─ Glioblastoma_IDH_wildtype associated_with EGFR_amplification
│   │   └─ Oligodendroglioma associated_with 1p19q_codeletion

├─ **progresses_to** (disease progression):
│   ├─ Definition: X progresses_to Y ≡ Disease X transforms into disease Y over time
│   ├─ Examples:
│   │   ├─ DiffuseAstrocytoma_IDH_mutant progresses_to AnaplasticAstrocytoma_IDH_mutant
│   │   ├─ AnaplasticAstrocytoma_IDH_mutant progresses_to Glioblastoma_IDH_mutant
│   │   └─ UnrupturedAneurysm progresses_to RupturedAneurysm

└─ **has_molecular_feature** (pathology-molecular marker):
    ├─ Definition: X has_molecular_feature Y ≡ Pathology X exhibits molecular marker Y
    ├─ Domain: PathologicalEntity
    ├─ Range: MolecularMarker
    ├─ Examples:
    │   ├─ Glioblastoma_IDH_wildtype has_molecular_feature EGFR_amplification
    │   ├─ Glioblastoma_IDH_wildtype has_molecular_feature MGMT_unmethylated
    │   ├─ Oligodendroglioma has_molecular_feature IDH_mutation
    │   ├─ Oligodendroglioma has_molecular_feature 1p19q_codeletion
    │   └─ DiffuseAstrocytoma has_molecular_feature TP53_mutation

---

### CLINICAL RELATIONSHIPS ⭐⭐⭐:

├─ **has_symptom** (pathology-symptom):
│   ├─ Definition: X has_symptom Y ≡ Pathology X manifests with symptom Y
│   ├─ Domain: PathologicalEntity
│   ├─ Range: Symptom
│   ├─ Examples:
│   │   ├─ Glioblastoma has_symptom Headache
│   │   ├─ Glioblastoma has_symptom Seizure
│   │   ├─ DiscHerniation has_symptom Radiculopathy
│   │   └─ NPH has_symptom GaitDisturbance

├─ **has_sign** (pathology-sign):
│   ├─ Definition: X has_sign Y ≡ Pathology X presents with objective sign Y
│   ├─ Domain: PathologicalEntity
│   ├─ Range: Sign
│   ├─ Examples:
│   │   ├─ StrokeInfarction has_sign Hemiparesis
│   │   ├─ CaudaEquinaSyndrome has_sign SaddleAnesthesia
│   │   └─ CN_III_PComA_Aneurysm has_sign PupilInvolving_CN_III_Palsy

├─ **has_imaging_finding** (pathology-imaging):
│   ├─ Definition: X has_imaging_finding Y ≡ Pathology X exhibits imaging characteristic Y
│   ├─ Domain: PathologicalEntity
│   ├─ Range: ImagingFinding
│   ├─ Examples:
│   │   ├─ Glioblastoma has_imaging_finding RingEnhancement
│   │   ├─ Glioblastoma has_imaging_finding ElevatedCBV
│   │   ├─ AcuteInfarction has_imaging_finding DWI_RestrictedDiffusion
│   │   ├─ Abscess has_imaging_finding RingEnhancement
│   │   ├─ Abscess has_imaging_finding DWI_RestrictedDiffusion
│   │   ├─ Meningioma has_imaging_finding HomogeneousEnhancement
│   │   └─ Meningioma has_imaging_finding DuralTail

├─ **diagnosed_by** (pathology-diagnostic test):
│   ├─ Definition: X diagnosed_by Y ≡ Pathology X is identified using diagnostic test Y
│   ├─ Domain: PathologicalEntity
│   ├─ Range: DiagnosticTest
│   ├─ Examples:
│   │   ├─ AcuteStroke diagnosed_by DWI_MRI
│   │   ├─ Aneurysm diagnosed_by CTA
│   │   ├─ Aneurysm diagnosed_by DSA
│   │   ├─ Glioblastoma diagnosed_by ContrastEnhancedMRI
│   │   └─ Oligodendroglioma diagnosed_by 1p19q_Testing

└─ **treated_by** (pathology-intervention):
    ├─ Definition: X treated_by Y ≡ Pathology X is managed using intervention Y
    ├─ Domain: PathologicalEntity
    ├─ Range: Intervention
    ├─ Examples:
    │   ├─ Glioblastoma treated_by GrossTotalResection
    │   ├─ Glioblastoma treated_by Temozolomide
    │   ├─ Glioblastoma treated_by ExternalBeamRadiotherapy
    │   ├─ Aneurysm treated_by MicrosurgicalClipping
    │   ├─ Aneurysm treated_by EndovascularCoiling
    │   ├─ DiscHerniation treated_by Microdiscectomy
    │   ├─ BrainMetastasis treated_by StereotacticRadiosurgery
    │   └─ NPH treated_by VentriculoperitonealShunt

---

### INTERVENTION RELATIONSHIPS ⭐⭐⭐:

├─ **targets** (intervention-pathology):
│   ├─ Definition: X targets Y ≡ Intervention X is directed at pathology Y
│   ├─ Domain: Intervention
│   ├─ Range: PathologicalEntity
│   ├─ Inverse: treated_by
│   ├─ Examples:
│   │   ├─ Temozolomide targets Glioblastoma
│   │   └─ MicrosurgicalClipping targets Aneurysm

├─ **has_complication** (intervention-complication):
│   ├─ Definition: X has_complication Y ≡ Intervention X may result in complication Y
│   ├─ Domain: Intervention
│   ├─ Range: Complication
│   ├─ Examples:
│   │   ├─ Craniotomy has_complication PostoperativeHemorrhage
│   │   ├─ Craniotomy has_complication Infection
│   │   ├─ Craniotomy has_complication Seizure
│   │   ├─ VentriculoperitonealShunt has_complication ShuntInfection
│   │   ├─ VentriculoperitonealShunt has_complication OverdrainageSDH
│   │   ├─ Temozolomide has_complication Myelosuppression
│   │   └─ ExternalBeamRadiotherapy has_complication RadiationNecrosis

├─ **requires** (intervention dependency):
│   ├─ Definition: X requires Y ≡ Intervention X necessitates intervention/resource Y
│   ├─ Examples:
│   │   ├─ GrossTotalResection requires ContrastEnhancedMRI (preoperative planning)
│   │   ├─ MicrosurgicalClipping requires DSA (aneurysm characterization)
│   │   ├─ AwakeCraniotomy requires fMRI (language mapping)
│   │   └─ StereotacticBiopsy requires Neuronavigation

└─ **achieves** (intervention-outcome):
    ├─ Definition: X achieves Y ≡ Intervention X produces outcome Y
    ├─ Domain: Intervention
    ├─ Range: Outcome
    ├─ Examples:
    │   ├─ GrossTotalResection_GBM achieves MedianSurvival_17months
    │   ├─ StuppProtocol achieves MedianSurvival_14.6months
    │   └─ Microdiscectomy achieves 80-90%_PainRelief

---

### DIAGNOSTIC RELATIONSHIPS ⭐⭐:

├─ **detects** (diagnostic test-pathology):
│   ├─ Definition: X detects Y ≡ Diagnostic test X identifies pathology Y
│   ├─ Domain: DiagnosticTest
│   ├─ Range: PathologicalEntity
│   ├─ Inverse: diagnosed_by
│   ├─ Examples:
│   │   ├─ DWI_MRI detects AcuteInfarction (sensitivity 90-95%)
│   │   ├─ CTA detects Aneurysm (sensitivity 95-98%)
│   │   └─ DSA detects Aneurysm (gold standard, sensitivity 98-100%)

└─ **reveals** (diagnostic test-finding):
    ├─ Definition: X reveals Y ≡ Diagnostic test X demonstrates finding Y
    ├─ Domain: DiagnosticTest
    ├─ Range: ImagingFinding or MolecularMarker
    ├─ Examples:
    │   ├─ ContrastEnhancedMRI reveals RingEnhancement
    │   ├─ DWI_MRI reveals RestrictedDiffusion
    │   └─ TumorSequencing reveals IDH_mutation

---

## IV. ATTRIBUTE SCHEMAS (DATA PROPERTIES) ⭐⭐⭐

### GENERAL ATTRIBUTES ⭐⭐⭐:

├─ **has_name** (rdfs:label):
│   ├─ Domain: Entity
│   ├─ Range: xsd:string
│   ├─ Example: Glioblastoma has_name "Glioblastoma, IDH-wildtype, WHO Grade 4"

├─ **has_synonym**:
│   ├─ Domain: Entity
│   ├─ Range: xsd:string
│   ├─ Examples:
│   │   ├─ Glioblastoma has_synonym "GBM"
│   │   ├─ InternalCapsule has_synonym "Capsula interna"
│   │   └─ AqueductOfSylvius has_synonym "Cerebral aqueduct"

├─ **has_definition**:
│   ├─ Domain: Entity
│   ├─ Range: xsd:string
│   ├─ Example: Glioblastoma has_definition "WHO Grade 4 diffuse astrocytic glioma characterized by..."

├─ **has_FMA_ID**:
│   ├─ Domain: AnatomicalEntity
│   ├─ Range: xsd:string (format: "FMA:######")
│   ├─ Example: InternalCapsulePosteriorLimb has_FMA_ID "FMA:62023"

├─ **has_SNOMED_CT_ID**:
│   ├─ Domain: PathologicalEntity | ClinicalFinding | Intervention
│   ├─ Range: xsd:string (format: "SNOMEDCT:########")
│   ├─ Example: Glioblastoma has_SNOMED_CT_ID "SNOMEDCT:393563007"

└─ **has_RadLex_ID**:
    ├─ Domain: ImagingFinding | AnatomicalEntity
    ├─ Range: xsd:string (format: "RadLex:RID####")
    ├─ Example: RingEnhancement has_RadLex_ID "RadLex:RID5741"

---

### ANATOMICAL ATTRIBUTES ⭐⭐:

├─ **has_laterality**:
│   ├─ Domain: AnatomicalStructure
│   ├─ Range: {Left, Right, Bilateral, Midline}
│   ├─ Examples:
│   │   ├─ LeftFrontalLobe has_laterality Left
│   │   ├─ CorpusCallosum has_laterality Midline
│   │   └─ OpticChiasm has_laterality Midline

├─ **has_brodmann_area**:
│   ├─ Domain: CerebralCortex
│   ├─ Range: xsd:integer (1-52)
│   ├─ Examples:
│   │   ├─ PrimaryMotorCortex has_brodmann_area 4
│   │   ├─ BrocasArea has_brodmann_area 44
│   │   ├─ BrocasArea has_brodmann_area 45
│   │   └─ WernickesArea has_brodmann_area 22

├─ **has_spinal_level**:
│   ├─ Domain: SpinalCord | SpinalNerve | VertebralColumn
│   ├─ Range: {C1-C8, T1-T12, L1-L5, S1-S5, Coccyx}
│   ├─ Examples:
│   │   ├─ CervicalEnlargement has_spinal_level C3-T1
│   │   └─ ConusModullaris has_spinal_level L1-L2_vertebral

└─ **has_vessel_segment**:
    ├─ Domain: CerebralArtery
    ├─ Range: xsd:string (e.g., "M1", "A1", "P1")
    ├─ Examples:
    │   ├─ MCA_M1 has_vessel_segment "M1"
    │   └─ ACA_A1 has_vessel_segment "A1"

---

### PATHOLOGY ATTRIBUTES ⭐⭐⭐:

├─ **has_WHO_grade**:
│   ├─ Domain: BrainTumor
│   ├─ Range: {1, 2, 3, 4}
│   ├─ Examples:
│   │   ├─ Glioblastoma has_WHO_grade 4
│   │   ├─ Oligodendroglioma has_WHO_grade 2 or 3
│   │   └─ PilocyticAstrocytoma has_WHO_grade 1

├─ **has_IDH_status**:
│   ├─ Domain: Glioma
│   ├─ Range: {IDH_mutant, IDH_wildtype}
│   ├─ Examples:
│   │   ├─ Glioblastoma_IDH_wildtype has_IDH_status IDH_wildtype
│   │   └─ Oligodendroglioma has_IDH_status IDH_mutant

├─ **has_MGMT_status**:
│   ├─ Domain: Glioblastoma
│   ├─ Range: {MGMT_methylated, MGMT_unmethylated}
│   ├─ Prognostic significance: MGMT_methylated → better TMZ response
│   ├─ Frequency: 40-45% methylated

├─ **has_1p19q_status**:
│   ├─ Domain: Glioma
│   ├─ Range: {1p19q_codeleted, 1p19q_intact}
│   ├─ Required for Oligodendroglioma diagnosis: IDH_mutant + 1p19q_codeleted

├─ **has_size_mm**:
│   ├─ Domain: PathologicalEntity
│   ├─ Range: xsd:float (millimeters)
│   ├─ Examples:
│   │   ├─ Aneurysm has_size_mm 7.5
│   │   ├─ Meningioma has_size_mm 35.0
│   │   └─ Metastasis has_size_mm 12.0

├─ **has_rupture_status** (aneurysms):
│   ├─ Domain: Aneurysm
│   ├─ Range: {Ruptured, Unruptured}

├─ **has_Spetzler_Martin_grade**:
│   ├─ Domain: AVM
│   ├─ Range: xsd:integer (1-5, or 6 for inoperable)
│   ├─ Components: Size (0-3 points), Eloquence (0-1), Venous drainage (0-1)

├─ **has_disc_herniation_type**:
│   ├─ Domain: DiscHerniation
│   ├─ Range: {Protrusion, Extrusion, Sequestration}

├─ **has_stenosis_severity**:
│   ├─ Domain: SpinalStenosis | VesselStenosis
│   ├─ Range: {Mild, Moderate, Severe}
│   ├─ Central canal stenosis: Severe <10mm

├─ **has_GCS_score** (Glasgow Coma Scale):
│   ├─ Domain: TraumaticBrainInjury
│   ├─ Range: xsd:integer (3-15)
│   ├─ Interpretation: Mild (13-15), Moderate (9-12), Severe (≤8)

└─ **has_ASIA_grade** (spinal cord injury):
    ├─ Domain: SpinalCordInjury
    ├─ Range: {ASIA_A, ASIA_B, ASIA_C, ASIA_D, ASIA_E}
    ├─ ASIA_A: Complete injury, no motor/sensory below level

---

### IMAGING ATTRIBUTES ⭐⭐⭐:

├─ **has_HU_value** (Hounsfield units):
│   ├─ Domain: CT_Finding
│   ├─ Range: xsd:float (-1000 to +3000)
│   ├─ Examples:
│   │   ├─ AcuteHemorrhage has_HU_value 50-90
│   │   ├─ GrayMatter has_HU_value 30-40
│   │   ├─ WhiteMatter has_HU_value 20-30
│   │   └─ Calcification has_HU_value >100

├─ **has_T1_signal**:
│   ├─ Domain: MRI_Finding
│   ├─ Range: {Hyperintense, Isointense, Hypointense}
│   ├─ Examples:
│   │   ├─ SubacuteHemorrhage has_T1_signal Hyperintense
│   │   └─ Edema has_T1_signal Hypointense

├─ **has_T2_signal**:
│   ├─ Domain: MRI_Finding
│   ├─ Range: {Hyperintense, Isointense, Hypointense}
│   ├─ Examples:
│   │   ├─ Edema has_T2_signal Hyperintense
│   │   └─ Hemosiderin has_T2_signal Hypointense

├─ **has_enhancement_pattern**:
│   ├─ Domain: ContrastEnhancement
│   ├─ Range: {Ring, Homogeneous, Heterogeneous, Nodular, None}
│   ├─ Examples:
│   │   ├─ Glioblastoma has_enhancement_pattern Ring
│   │   ├─ Meningioma has_enhancement_pattern Homogeneous
│   │   └─ LowGradeGlioma has_enhancement_pattern None

├─ **has_ADC_value** (apparent diffusion coefficient):
│   ├─ Domain: DWI_Finding
│   ├─ Range: xsd:float (×10⁻⁶ mm²/s)
│   ├─ Normal brain: 700-900
│   ├─ Restricted diffusion: <700 (acute infarct, abscess)
│   ├─ Facilitated diffusion: >1000 (vasogenic edema, necrosis)

├─ **has_CBV_value** (cerebral blood volume):
│   ├─ Domain: PerfusionMRI_Finding
│   ├─ Range: xsd:float (mL/100g)
│   ├─ Normal: 4-5 mL/100g
│   ├─ High-grade glioma: ↑↑ CBV (angiogenesis)
│   ├─ Low-grade glioma: Normal or ↓ CBV

├─ **has_FA_value** (fractional anisotropy):
│   ├─ Domain: DTI_Finding
│   ├─ Range: xsd:float (0-1)
│   ├─ White matter tracts: 0.6-0.8 (high directionality)
│   ├─ Gray matter: 0.2-0.3 (low directionality)
│   ├─ Tumor infiltration: ↓ FA (disrupted white matter)

└─ **has_ASPECTS_score** (Alberta Stroke Program Early CT Score):
    ├─ Domain: AcuteIschemicStroke
    ├─ Range: xsd:integer (0-10)
    ├─ Interpretation: ≥6 → favorable for thrombectomy
    ├─ Scoring: 10 regions in MCA territory, -1 per region with early ischemic changes

---

### TREATMENT ATTRIBUTES ⭐⭐⭐:

├─ **has_extent_of_resection**:
│   ├─ Domain: TumorResection
│   ├─ Range: {GTR_>98%, STR_80-98%, Partial_<80%, Biopsy}
│   ├─ Prognostic: GTR associated with longer survival

├─ **has_radiation_dose_Gy**:
│   ├─ Domain: RadiationTherapy
│   ├─ Range: xsd:float (Gray)
│   ├─ Examples:
│   │   ├─ GBM_EBRT has_radiation_dose_Gy 60.0
│   │   ├─ SRS_Metastasis has_radiation_dose_Gy 18.0
│   │   └─ SRS_AVM has_radiation_dose_Gy 20.0

├─ **has_fractionation_number**:
│   ├─ Domain: ExternalBeamRadiotherapy
│   ├─ Range: xsd:integer
│   ├─ Examples:
│   │   ├─ GBM_standard has_fractionation_number 30 (60 Gy / 2 Gy per fraction)
│   │   └─ SRS has_fractionation_number 1 (single fraction)

├─ **has_chemotherapy_dose**:
│   ├─ Domain: Chemotherapy
│   ├─ Range: xsd:string (with units)
│   ├─ Examples:
│   │   ├─ Temozolomide_concurrent has_chemotherapy_dose "75 mg/m²/day"
│   │   └─ Temozolomide_adjuvant has_chemotherapy_dose "150-200 mg/m² days 1-5/28"

├─ **has_DBS_target**:
│   ├─ Domain: DeepBrainStimulation
│   ├─ Range: {STN, GPi, VIM, Thalamus}
│   ├─ Examples:
│   │   ├─ DBS_Parkinsons has_DBS_target STN
│   │   └─ DBS_EssentialTremor has_DBS_target VIM

└─ **has_surgical_approach**:
    ├─ Domain: SurgicalProcedure
    ├─ Range: xsd:string
    ├─ Examples:
    │   ├─ AneurysmClipping has_surgical_approach "Pterional"
    │   ├─ PituitaryAdenoma has_surgical_approach "Transsphenoidal"
    │   └─ FourthVentricle_Tumor has_surgical_approach "Suboccipital"

---

### OUTCOME ATTRIBUTES ⭐⭐⭐:

├─ **has_median_survival_months**:
│   ├─ Domain: Neoplasm | TreatmentProtocol
│   ├─ Range: xsd:float (months)
│   ├─ Examples:
│   │   ├─ Glioblastoma_IDH_wildtype has_median_survival_months 12-15
│   │   ├─ Glioblastoma_IDH_mutant has_median_survival_months 24-31
│   │   ├─ StuppProtocol has_median_survival_months 14.6
│   │   └─ Oligodendroglioma has_median_survival_months 120-180

├─ **has_KPS_score** (Karnofsky Performance Status):
│   ├─ Domain: Patient | ClinicalOutcome
│   ├─ Range: xsd:integer (0-100, increments of 10)
│   ├─ Interpretation: 100 (normal), 70-80 (independent), <50 (requires assistance)

├─ **has_mRS_score** (modified Rankin Scale):
│   ├─ Domain: StrokeOutcome
│   ├─ Range: xsd:integer (0-6)
│   ├─ Interpretation: 0 (no symptoms), 3 (moderate disability), 6 (death)

├─ **has_GOS_score** (Glasgow Outcome Scale):
│   ├─ Domain: TraumaticBrainInjury
│   ├─ Range: xsd:integer (1-5, or 1-8 for extended GOS)
│   ├─ Interpretation: 5/8 (good recovery), 3 (severe disability), 1 (death)

├─ **has_complication_rate_percent**:
│   ├─ Domain: Intervention | Complication
│   ├─ Range: xsd:float (0-100)
│   ├─ Examples:
│   │   ├─ Craniotomy has_complication_rate_percent 5-10 (infection)
│   │   ├─ VPshunt has_complication_rate_percent 5-10 (infection)
│   │   └─ EndovascularCoiling has_complication_rate_percent 3-5 (rerupture)

└─ **has_recurrence_rate_percent**:
    ├─ Domain: Neoplasm | TumorResection
    ├─ Range: xsd:float (0-100)
    ├─ Examples:
    │   ├─ Glioblastoma_PostResection has_recurrence_rate_percent 100 (nearly universal)
    │   ├─ Meningioma_Grade1_SimpsonI has_recurrence_rate_percent 10-year: 9%
    │   ├─ Meningioma_Grade1_SimpsonIV has_recurrence_rate_percent 10-year: 40%
    │   └─ Microdiscectomy has_recurrence_rate_percent 5-10

---

## V. QUERY PATTERNS FOR CLINICAL DECISION SUPPORT ⭐⭐⭐

### DIFFERENTIAL DIAGNOSIS QUERIES ⭐⭐⭐:

**Query 1: Ring-enhancing lesion differential diagnosis**

```sparql
# Find all pathologies that exhibit ring enhancement on MRI
SELECT ?pathology ?additionalFinding ?location
WHERE {
  ?pathology rdf:type ont:PathologicalEntity .
  ?pathology ont:has_imaging_finding ont:RingEnhancement .
  OPTIONAL { ?pathology ont:has_imaging_finding ?additionalFinding }
  OPTIONAL { ?pathology ont:has_location ?location }
}
# Results:
# - Glioblastoma: Ring enhancement + Elevated CBV + Necrosis
# - Metastasis: Ring enhancement + Multiple lesions + Edema
# - Abscess: Ring enhancement + Restricted diffusion (DWI) ⭐ KEY DISCRIMINATOR
# - Subacute infarct: Gyral enhancement + Restricted diffusion (timing)
# - Toxoplasmosis: Multiple ring-enhancing lesions + Basal ganglia
```

**Query 2: Restricted diffusion differential diagnosis**

```sparql
# Find pathologies with restricted diffusion on DWI/ADC
SELECT ?pathology ?T1_signal ?T2_signal ?enhancement
WHERE {
  ?pathology ont:has_imaging_finding ont:DWI_RestrictedDiffusion .
  OPTIONAL { ?pathology ont:has_imaging_finding ?t1 . ?t1 ont:has_T1_signal ?T1_signal }
  OPTIONAL { ?pathology ont:has_imaging_finding ?t2 . ?t2 ont:has_T2_signal ?T2_signal }
  OPTIONAL { ?pathology ont:has_imaging_finding ?enh . ?enh ont:has_enhancement_pattern ?enhancement }
}
# Results:
# - Acute infarction ⭐: DWI bright, ADC dark, no enhancement (first 24-48h)
# - Abscess: DWI bright, ADC dark, ring enhancement
# - Epidermoid cyst: DWI bright, ADC dark, no enhancement, T1 hypointense
# - Hypercellular tumor (lymphoma, medulloblastoma): DWI bright (moderate)
```

**Query 3: Identify pathologies causing specific symptom**

```sparql
# Find pathologies causing foot drop
SELECT ?pathology ?location ?treatment
WHERE {
  ?pathology ont:has_symptom ont:FootDrop .
  ?pathology ont:has_location ?location .
  ?pathology ont:treated_by ?treatment .
}
# Results:
# - L5 radiculopathy (L4-L5 disc herniation) ⭐ most common
#   Location: L4_L5_intervertebral_disc
#   Treatment: Conservative 6-12 weeks → Microdiscectomy if refractory
# - Common peroneal nerve injury
#   Location: Fibular_head
# - L5 nerve root tumor
```

---

### TREATMENT SELECTION QUERIES ⭐⭐⭐:

**Query 4: Optimal treatment for glioblastoma based on molecular features**

```sparql
# Treatment selection based on IDH status and MGMT methylation
SELECT ?treatment ?median_survival ?complication_rate
WHERE {
  ?tumor rdf:type ont:Glioblastoma_IDH_wildtype .
  ?tumor ont:has_MGMT_status ?MGMT .
  ?tumor ont:treated_by ?treatment .
  ?treatment ont:achieves ?outcome .
  ?outcome ont:has_median_survival_months ?median_survival .
  ?treatment ont:has_complication ?complication .
  ?complication ont:has_complication_rate_percent ?complication_rate .
  FILTER (?MGMT = ont:MGMT_methylated)
}
# Results (MGMT methylated):
# 1. Maximal safe resection (5-ALA guided) ⭐
#    - GTR: Median survival 21-24 months
#    - Complications: Infection 5%, permanent deficit 3-5%
# 2. Concurrent chemoradiotherapy (Stupp protocol)
#    - Temozolomide 75 mg/m² + 60 Gy / 30 fractions
#    - Median survival 21.7 months (MGMT methylated)
# 3. Adjuvant temozolomide (6-12 cycles)
#    - 150-200 mg/m² days 1-5/28
# 4. TTFields (Tumor Treating Fields)
#    - Added to adjuvant TMZ: Median survival 20.9 months

# Results (MGMT unmethylated):
# Same surgical approach, but:
# - Median survival 12-15 months (poorer response to TMZ)
# - Consider clinical trials, alternative regimens
```

**Query 5: Aneurysm treatment selection (clipping vs coiling)**

```sparql
# Select treatment modality based on aneurysm characteristics
SELECT ?treatment ?success_rate ?complication_rate
WHERE {
  ?aneurysm rdf:type ont:Aneurysm .
  ?aneurysm ont:has_location ?location .
  ?aneurysm ont:has_size_mm ?size .
  ?aneurysm ont:has_morphology ?morphology .
  ?aneurysm ont:treated_by ?treatment .
  ?treatment ont:achieves ?outcome .
  ?outcome ont:has_success_rate_percent ?success_rate .
  ?treatment ont:has_complication_rate_percent ?complication_rate .
}
# Decision tree (based on ISAT trial + meta-analyses):
#
# AComA aneurysm, small (<7mm), narrow neck:
#   - Coiling preferred ⭐ (easier access, lower morbidity)
#   - Success: 85-90%, Recanalization: 20-30%, Retreatment: 10-15%
#   - Clipping alternative: Success 95%, Recurrence <5%
#
# MCA aneurysm, M1 bifurcation, wide neck:
#   - Clipping preferred ⭐ (better for wide neck, branch incorporation)
#   - Success: 95%, Permanent deficit: 5-8%
#   - Coiling with stent/balloon assist: Higher technical difficulty
#
# Basilar apex aneurysm, large (>10mm):
#   - Coiling preferred (deep location, difficult surgical access)
#   - Flow diversion for giant aneurysms
#   - Clipping: Higher cranial nerve palsy risk (CN III, VI)
```

---

### PROGNOSIS PREDICTION QUERIES ⭐⭐⭐:

**Query 6: Predict survival for glioblastoma patient**

```sparql
# Calculate prognostic factors for GBM
SELECT ?factor ?impact_on_survival
WHERE {
  ?patient rdf:type ont:GBM_Patient .
  ?patient ont:has_age ?age .
  ?patient ont:has_KPS_score ?kps .
  ?patient ont:has_tumor ?tumor .
  ?tumor ont:has_IDH_status ?idh .
  ?tumor ont:has_MGMT_status ?mgmt .
  ?tumor ont:has_extent_of_resection ?eor .
}
# Prognostic model (multivariable):
#
# Favorable factors (↑ survival):
# - Age <50 years: +6-8 months median survival
# - KPS ≥70: +4-6 months
# - IDH-mutant: +12-15 months ⭐
# - MGMT methylated: +6-9 months ⭐
# - GTR (>98%): +4-6 months vs STR
# - Frontal/temporal location: +2-3 months vs deep/eloquent
#
# Unfavorable factors (↓ survival):
# - Age >65 years: -4-6 months
# - KPS <70: -4-6 months
# - Multifocal disease: -6-8 months
# - Subventricular zone involvement: -3-4 months
#
# Example calculation:
# 55-year-old, KPS 80, IDH-wildtype, MGMT methylated, GTR
# Base (IDH-wildtype): 12 months
# + MGMT methylated: +7 months
# + GTR: +5 months
# + KPS 80: +3 months
# Predicted median survival: ~27 months
```

**Query 7: Stroke outcome prediction (mRS at 90 days)**

```sparql
# Predict functional outcome after thrombectomy
SELECT ?predictor ?mRS_0-2_probability
WHERE {
  ?patient rdf:type ont:AcuteStrokePatient .
  ?patient ont:has_age ?age .
  ?patient ont:has_baseline_mRS ?baseline_mRS .
  ?stroke ont:has_NIHSS_score ?nihss .
  ?stroke ont:has_ASPECTS_score ?aspects .
  ?stroke ont:has_location ont:MCA_M1_occlusion .
  ?stroke ont:has_time_to_treatment_minutes ?time .
  ?stroke ont:treated_by ont:MechanicalThrombectomy .
}
# Outcome prediction (mRS 0-2 = good outcome):
#
# Favorable predictors:
# - ASPECTS ≥6: Good outcome 50-60% ⭐
# - Time to treatment <6h: Good outcome 60-70%
# - NIHSS <10: Good outcome 70-80%
# - Age <70: Good outcome 55-65%
# - Successful recanalization (TICI 2b-3): Good outcome 60-70% ⭐
#
# Unfavorable predictors:
# - ASPECTS <6: Good outcome 20-30%
# - Time to treatment >6h: Good outcome 30-40%
# - NIHSS >20: Good outcome 15-25%
# - Age >80: Good outcome 20-30%
# - Failed recanalization (TICI 0-1): Good outcome 10-15%
```

---

### COMPLICATION RISK QUERIES ⭐⭐:

**Query 8: Assess surgical complication risk**

```sparql
# Calculate risk of permanent neurological deficit for tumor resection
SELECT ?risk_factor ?deficit_risk_percent
WHERE {
  ?tumor ont:has_location ?location .
  ?location ont:adjacent_to ?eloquent_structure .
  ?tumor ont:has_size_mm ?size .
  ?surgery ont:requires ?adjunct_technique .
  ?surgery ont:has_complication ?complication .
  ?complication rdf:type ont:NeurologicalDeficit .
}
# Risk stratification:
#
# Low risk (<5% permanent deficit):
# - Convexity lesion, non-eloquent (frontal pole, temporal pole, occipital)
# - Small size (<3 cm)
# - Well-demarcated (meningioma, metastasis)
#
# Moderate risk (5-15%):
# - Adjacent to eloquent cortex (motor, speech, visual)
# - With adjuncts: Awake mapping, fMRI, DTI tractography ⭐ (risk ↓ by 50%)
# - Moderate size (3-5 cm)
#
# High risk (>15%):
# - Infiltrative glioma in eloquent cortex
# - Deep location (thalamus, basal ganglia, brainstem)
# - Large size (>5 cm) with mass effect
# - Without functional mapping: Risk 20-30%
```

---

## VI. TEMPORAL RELATIONSHIPS ⭐⭐⭐

### DISEASE PROGRESSION TIMELINES ⭐⭐⭐:

├─ **Glioma progression sequence** (IDH-mutant astrocytoma):
│   ├─ DiffuseAstrocytoma_Grade2 (median time: 5-7 years)
│   │   ↓ progresses_to
│   ├─ AnaplasticAstrocytoma_Grade3 (median time: 3-5 years)
│   │   ↓ progresses_to
│   └─ Glioblastoma_IDH_mutant_Grade4 (median survival: 24-31 months)

├─ **Oligodendroglioma progression** (slower):
│   ├─ Oligodendroglioma_Grade2 (median time to progression: 8-12 years)
│   │   ↓ progresses_to
│   └─ AnaplasticOligodendroglioma_Grade3 (median survival: 10-15 years from diagnosis)

├─ **Aneurysm natural history**:
│   ├─ UnrupturedAneurysm
│   │   ├─ Rupture risk (per year):
│   │   │   ├─ Small (<7mm): 0.5-1% per year
│   │   │   ├─ Large (7-24mm): 2-3% per year
│   │   │   └─ Giant (≥25mm): 6-10% per year
│   │   ↓ may_progress_to (cumulative risk: PHASES score)
│   └─ RupturedAneurysm (SAH)
│       ├─ Acute phase (0-3 days): Rerupture risk 15-20% without treatment ⭐
│       ├─ Vasospasm window (days 4-14): Peak day 7
│       └─ Chronic (>3 weeks): Hydrocephalus risk 20-30%

├─ **Disc herniation natural history**:
│   ├─ Acute phase (0-6 weeks):
│   │   ├─ Natural resolution: 30-40% (resorption)
│   │   └─ Conservative management: 70-90% improve
│   ├─ Subacute (6-12 weeks):
│   │   └─ Persistent symptoms: Consider surgery
│   └─ Chronic (>12 weeks):
│       └─ If no improvement: Microdiscectomy (80-90% success)

└─ **Stroke timeline** (ischemic):
    ├─ Hyperacute (0-6h):
    │   ├─ DWI positive within 30 minutes
    │   ├─ Thrombolysis window: 0-4.5h (tPA) ⭐
    │   ├─ Thrombectomy window: 0-24h (with imaging selection)
    │   └─ Penumbra salvageable
    ├─ Acute (6h-7 days):
    │   ├─ Core: Established infarction
    │   ├─ Edema: Peaks 48-72h (mass effect risk)
    │   └─ Hemorrhagic transformation: Risk 5-10% (higher with thrombolysis)
    ├─ Subacute (1-3 weeks):
    │   ├─ Fogging effect on CT: Infarct becomes isodense
    │   └─ Gyral enhancement: BBB disruption
    └─ Chronic (>3 weeks):
        ├─ Encephalomalacia: Cystic changes, gliosis
        └─ Wallerian degeneration: Downstream tract degeneration

---

### TREATMENT SEQUENCING ⭐⭐⭐:

├─ **Glioblastoma treatment timeline (Stupp protocol)** ⭐⭐⭐:
│   ├─ Week 0-1: Surgery (maximal safe resection)
│   │   └─ Histopathological diagnosis + molecular testing (IDH, MGMT, 1p/19q)
│   ├─ Week 3-4: Initiate concurrent chemoradiotherapy
│   │   ├─ Radiation: 60 Gy / 30 fractions (6 weeks)
│   │   ├─ Temozolomide: 75 mg/m² daily (including weekends)
│   │   └─ Dexamethasone: Taper as tolerated
│   ├─ Week 10: 4-week break (allow marrow recovery)
│   ├─ Week 14-52: Adjuvant temozolomide (6 cycles)
│   │   ├─ Cycle 1: 150 mg/m² days 1-5/28 (if ANC >1500, platelets >100k)
│   │   └─ Cycles 2-6: 200 mg/m² days 1-5/28 (if tolerated)
│   ├─ Extended adjuvant (some centers): Cycles 7-12
│   └─ TTFields: Initiate with adjuvant TMZ, continue ≥18 months

├─ **Metastatic brain tumor treatment sequence** ⭐⭐:
│   ├─ Limited metastases (1-4 lesions):
│   │   ├─ Surgery (resection) for accessible lesions >3 cm
│   │   │   └─ Postoperative SRS to cavity (preferred over WBRT)
│   │   ├─ SRS for lesions 1-3 cm, or multiple lesions
│   │   │   └─ Dose: 18-24 Gy single fraction (size-dependent)
│   │   └─ Systemic therapy (concurrent or sequential)
│   │       ├─ EGFR+ NSCLC: Osimertinib (CNS penetrant)
│   │       ├─ ALK+ NSCLC: Alectinib
│   │       └─ BRAF V600E melanoma: Dabrafenib + Trametinib
│   └─ Extensive metastases (>4 lesions):
│       ├─ Consider WBRT (if good performance status)
│       └─ Systemic therapy first-line

├─ **Aneurysmal SAH management timeline** ⭐⭐⭐:
│   ├─ Day 0 (ictus):
│   │   ├─ NCCT → CTA → DSA (if needed for surgical planning)
│   │   ├─ Secure aneurysm within 24h ⭐: Coiling or clipping
│   │   ├─ Initiate nimodipine 60 mg PO q4h × 21 days ⭐
│   │   └─ Blood pressure control: SBP <160 mmHg (pre-securing)
│   ├─ Days 1-3 (acute):
│   │   ├─ Post-securing: Maintain euvolemia, normotension
│   │   └─ Monitor for rebleeding (rare if secured), hydrocephalus
│   ├─ Days 4-14 (vasospasm window):
│   │   ├─ TCD monitoring: Daily (MCA velocity >120 cm/s concerning)
│   │   ├─ Clinical monitoring: Neuro checks q1-2h
│   │   ├─ Delayed cerebral ischemia (DCI): 20-30% incidence
│   │   │   └─ Treatment: Induced hypertension (SBP 160-200), IA vasodilators
│   │   └─ CTP if DCI suspected: Assess perfusion deficits
│   └─ Days 14-21:
│       └─ Vasospasm risk ↓, continue nimodipine to day 21

└─ **Lumbar disc herniation treatment algorithm** ⭐⭐:
    ├─ Acute phase (0-6 weeks):
    │   ├─ Conservative management (unless cauda equina):
    │   │   ├─ NSAIDs, activity modification (avoid prolonged bed rest)
    │   │   ├─ Physical therapy (after 2-3 weeks)
    │   │   └─ Epidural steroid injection (if refractory)
    │   └─ Cauda equina syndrome: EMERGENCY surgery within 24-48h ⭐
    ├─ Subacute (6-12 weeks):
    │   └─ If persistent radiculopathy: Consider microdiscectomy
    └─ Surgical outcomes:
        ├─ SPORT trial: Surgery superior short-term (3-6 months)
        └─ Long-term (2-4 years): Both groups similar (30% crossover)

---

## VII. PROBABILISTIC RELATIONSHIPS ⭐⭐⭐

### RISK FACTORS (EPIDEMIOLOGICAL) ⭐⭐⭐:

├─ **Brain tumor risk factors**:
│   ├─ Glioblastoma:
│   │   ├─ Ionizing radiation exposure: RR 2.0-3.0 (dose-dependent)
│   │   ├─ Family history (rare): RR 1.5-2.0
│   │   └─ Genetic syndromes: Li-Fraumeni (TP53), Lynch syndrome (MMR genes)
│   ├─ Meningioma:
│   │   ├─ Female sex: 2:1 female:male ratio (hormone receptors)
│   │   ├─ Ionizing radiation: RR 6.0-10.0 (latency 20-30 years)
│   │   ├─ NF2 mutation: 50% develop meningioma
│   │   └─ Obesity: RR 1.2-1.3
│   └─ Metastatic brain tumors:
│       ├─ Primary cancer with CNS tropism:
│       │   ├─ Melanoma: 40-60% develop brain mets (highest propensity)
│       │   ├─ Lung cancer: 40-50% (most common source)
│       │   └─ Breast cancer: 15-20% (increasing with HER2+)

├─ **Aneurysm risk factors** (formation and rupture):
│   ├─ Formation risk:
│   │   ├─ Hypertension: OR 2.0-3.0
│   │   ├─ Smoking: OR 2.0-4.0
│   │   ├─ Female sex: 1.6:1 female:male
│   │   ├─ Family history (≥2 FDR): OR 4.0-8.0
│   │   └─ Genetic: PKD (polycystic kidney disease) 10-20%, ADPKD
│   ├─ Rupture risk (PHASES score):
│   │   ├─ Population: Japanese/Finnish > Caucasian
│   │   ├─ Hypertension: HR 2.0
│   │   ├─ Age: >70 years HR 1.5
│   │   ├─ Size: <7mm (1%/yr), 7-12mm (3%/yr), >12mm (6%/yr)
│   │   ├─ Earlier SAH: HR 2.5
│   │   └─ Site: PComA, basilar tip > AComA, MCA

├─ **Stroke risk factors**:
│   ├─ Modifiable:
│   │   ├─ Hypertension: RR 3.0-5.0 (single most important) ⭐
│   │   ├─ Atrial fibrillation: RR 5.0 (cardioembolic)
│   │   ├─ Diabetes: RR 1.8-3.0
│   │   ├─ Smoking: RR 2.0-4.0
│   │   ├─ Hyperlipidemia: RR 1.5-2.0
│   │   └─ Obesity: RR 1.3-1.5
│   └─ Non-modifiable:
│       ├─ Age: Each decade >55 years: RR doubles
│       ├─ Male sex: RR 1.25
│       └─ Family history: RR 1.3-1.5

└─ **Disc herniation risk factors**:
    ├─ Age: Peak 30-50 years
    ├─ Occupational: Heavy lifting, vibration exposure OR 2.0-3.0
    ├─ Smoking: OR 1.5-2.0 (disc degeneration)
    ├─ Obesity: OR 1.3-1.5 (increased load)
    └─ Genetic: Family history OR 2.0-4.0 (collagen disorders)

---

### PROGNOSTIC FACTORS (WITH HAZARD RATIOS) ⭐⭐⭐:

├─ **Glioblastoma prognostic factors** (multivariable Cox regression):
│   ├─ Molecular (strongest):
│   │   ├─ IDH-mutant vs IDH-wildtype: HR 0.3-0.4 (60-70% ↓ mortality) ⭐⭐
│   │   ├─ MGMT methylated vs unmethylated: HR 0.5-0.6 (40-50% ↓ mortality) ⭐⭐
│   │   ├─ G-CIMP (CpG island methylator phenotype): HR 0.4 (favorable)
│   │   └─ EGFR amplification: HR 1.3-1.5 (unfavorable)
│   ├─ Clinical:
│   │   ├─ Age <50 vs >65: HR 0.4-0.5 (50-60% ↓ mortality)
│   │   ├─ KPS ≥70 vs <70: HR 0.5-0.6
│   │   └─ Frontal/temporal vs deep/brainstem: HR 0.7 (favorable)
│   ├─ Treatment:
│   │   ├─ GTR (>98%) vs STR: HR 0.6-0.7 (30-40% ↓ mortality) ⭐
│   │   ├─ Stupp protocol vs RT alone: HR 0.63 (37% ↓ mortality) ⭐
│   │   └─ TTFields + TMZ vs TMZ alone: HR 0.63 (37% ↓ mortality)
│   └─ Tumor characteristics:
│       ├─ Subventricular zone contact: HR 1.5-2.0 (unfavorable)
│       ├─ Multifocal vs unifocal: HR 1.8-2.2
│       └─ Size >5cm vs <3cm: HR 1.3-1.5

├─ **Aneurysmal SAH prognostic factors** (mortality and outcome):
│   ├─ Clinical grade (strongest predictor) ⭐:
│   │   ├─ Hunt-Hess I-II: Mortality 5-10%, Good outcome 80-90%
│   │   ├─ Hunt-Hess III: Mortality 15-20%, Good outcome 60-70%
│   │   ├─ Hunt-Hess IV: Mortality 40-50%, Good outcome 30-40%
│   │   └─ Hunt-Hess V: Mortality 70-80%, Good outcome 10-15%
│   ├─ Radiographic (modified Fisher scale):
│   │   ├─ Fisher 1-2: Vasospasm risk 10-20%
│   │   ├─ Fisher 3-4: Vasospasm risk 40-60% ⭐
│   │   └─ Thick clot in cisterns/fissures: Highest vasospasm risk
│   ├─ Age:
│   │   ├─ <50 years: Good outcome 70-80%
│   │   └─ >70 years: Good outcome 20-30%, HR 2.0-3.0 for mortality
│   ├─ Aneurysm size:
│   │   ├─ Small (<10mm): Better outcome
│   │   └─ Large (>10mm): HR 1.5-2.0 (higher rerupture, worse grade)
│   └─ Complications:
│       ├─ Rerupture: Mortality 70-80% ⭐
│       ├─ Delayed cerebral ischemia: HR 2.0-3.0
│       └─ Hydrocephalus: May require shunt (20-30%)

├─ **Ischemic stroke prognostic factors** (mRS 0-2 at 90 days):
│   ├─ Imaging:
│   │   ├─ ASPECTS ≥6: Good outcome 50-60% ⭐
│   │   ├─ ASPECTS <6: Good outcome 20-30%
│   │   ├─ Core <70 mL: OR 3.0 for good outcome
│   │   └─ Mismatch ratio >1.8: Salvageable penumbra ⭐
│   ├─ Clinical:
│   │   ├─ NIHSS <10: Good outcome 70-80%
│   │   ├─ NIHSS 10-20: Good outcome 40-50%
│   │   ├─ NIHSS >20: Good outcome 15-25%
│   │   └─ Age <70 vs >80: OR 2.0-3.0 for good outcome
│   ├─ Treatment:
│   │   ├─ Successful recanalization (TICI 2b-3): OR 4.0-6.0 ⭐⭐
│   │   ├─ Time to treatment <6h vs >6h: OR 2.0
│   │   └─ Thrombolysis + thrombectomy vs thrombectomy alone: OR 1.3-1.5
│   └─ Complications:
│       ├─ Hemorrhagic transformation: mRS 5-6 in 60-70%
│       └─ Malignant edema: Mortality 60-80% without hemicraniectomy

└─ **Meningioma recurrence prognostic factors**:
    ├─ Simpson grade (resection extent) ⭐⭐:
    │   ├─ Grade I (GTR + dural origin + bone): 10-year recurrence 9%
    │   ├─ Grade II (GTR + coagulated dural): 10-year recurrence 16%
    │   ├─ Grade III (GTR, no dural manipulation): 10-year recurrence 29%
    │   ├─ Grade IV (subtotal resection): 10-year recurrence 40%
    │   └─ Grade V (biopsy, decompression): 10-year recurrence >80%
    ├─ WHO grade:
    │   ├─ Grade 1: 5-year recurrence 5-10%
    │   ├─ Grade 2 (atypical): 5-year recurrence 30-40%, HR 3.0
    │   └─ Grade 3 (anaplastic): 5-year recurrence >60%, HR 8.0-10.0
    ├─ Molecular:
    │   ├─ NF2 loss: HR 2.0 (higher recurrence)
    │   └─ TERT promoter mutation: HR 4.0-6.0 (aggressive)
    └─ Location:
        ├─ Skull base (cavernous sinus, petroclival): Higher recurrence (STR more common)
        └─ Convexity: Lower recurrence (GTR more achievable)

---

## VIII. REASONING RULES AND INFERENCE PATTERNS ⭐⭐⭐

### OWL AXIOMS (DESCRIPTION LOGIC) ⭐⭐⭐:

**Rule 1: Glioblastoma classification (WHO 2021)**

```owl
# Glioblastoma, IDH-wildtype definition
Glioblastoma_IDH_wildtype ≡ Glioma
  ∧ (has_IDH_status value IDH_wildtype)
  ∧ (has_WHO_grade value 4)
  ∧ (∃ has_molecular_feature . (EGFR_amplification ⊔ TERT_promoter_mutation))

# Inference: Any glioma with IDH-wildtype + Grade 4 → classify as Glioblastoma_IDH_wildtype
```

**Rule 2: Oligodendroglioma diagnostic criteria**

```owl
# Oligodendroglioma REQUIRED molecular features
Oligodendroglioma ≡ Glioma
  ∧ (has_IDH_status value IDH_mutant)
  ∧ (has_1p19q_status value 1p19q_codeleted)
  ∧ (has_WHO_grade value {2, 3})

# Inference: If glioma is IDH-mutant but 1p19q-intact → NOT oligodendroglioma (likely astrocytoma)
```

**Rule 3: Ring-enhancing lesion with restricted diffusion → Abscess**

```owl
# High likelihood abscess if both features present
Abscess ≡ CNS_Infection
  ∧ (has_imaging_finding value RingEnhancement)
  ∧ (has_imaging_finding value DWI_RestrictedDiffusion)
  ∧ (has_enhancement_pattern value SmoothRim)

# Inference: RingEnhancement + RestrictedDiffusion → strongly suggests Abscess (vs Glioblastoma or Metastasis)
# Glioblastoma: RingEnhancement + ElevatedCBV + IrregularRim (but NO restricted diffusion)
```

**Rule 4: Cauda equina syndrome surgical urgency**

```owl
# Emergency surgery required
CaudaEquinaSyndrome ≡ SpinalCordInjury
  ∧ (has_symptom value SaddleAnesthesia)
  ∧ (has_symptom value BladderDysfunction)
  ∧ (has_location value LumbarSpine)

# Inference: CaudaEquinaSyndrome → treated_by EmergencyDecompression (within 24-48h)
# Rule: IF CaudaEquinaSyndrome THEN requires (Microdiscectomy AND TimeToSurgery < 48h)
```

**Rule 5: Aneurysm treatment selection**

```owl
# Coiling preferred for posterior circulation
AneurysmCoilingPreferred ≡ Aneurysm
  ∧ (has_location value PosteriorCirculation)
  ∧ (has_morphology value NarrowNeck)
  ∧ (has_size_mm ≤ 10.0)

# Inference: Basilar apex aneurysm, small, narrow neck → EndovascularCoiling preferred (deep location)
```

---

### SWRL RULES (SEMANTIC WEB RULE LANGUAGE) ⭐⭐:

**Rule 6: Eloquent cortex identification**

```swrl
# IF tumor adjacent to eloquent structure, THEN high-risk surgery
Tumor(?t) ∧ has_location(?t, ?loc) ∧ adjacent_to(?loc, ?eloquent)
∧ EloquentCortex(?eloquent)
→ requires(?t, FunctionalMapping) ∧ has_surgical_risk(?t, High)

# Examples of EloquentCortex: PrimaryMotorCortex, BrocasArea, WernickesArea, CorticospinalTract
```

**Rule 7: Stroke thrombolysis eligibility**

```swrl
# Thrombolysis (tPA) eligibility criteria
AcuteStroke(?s) ∧ has_time_from_onset(?s, ?time) ∧ lessThan(?time, 270) # <4.5h
∧ has_NIHSS_score(?s, ?nihss) ∧ greaterThan(?nihss, 4) # NIHSS >4
∧ not(has_imaging_finding(?s, Hemorrhage)) # No hemorrhage on CT
∧ has_age(?patient, ?age) ∧ lessThan(?age, 80)
→ eligible_for(?s, Thrombolysis_tPA)

# Contraindications: Hemorrhage, recent surgery, anticoagulation (INR >1.7)
```

**Rule 8: Glioblastoma treatment protocol**

```swrl
# Stupp protocol eligibility
Glioblastoma(?g) ∧ has_patient(?g, ?p) ∧ has_KPS_score(?p, ?kps) ∧ greaterThan(?kps, 60)
∧ has_age(?p, ?age) ∧ lessThan(?age, 70)
∧ treated_by(?g, GrossTotalResection)
→ treated_by(?g, StuppProtocol) ∧ treated_by(?g, Temozolomide) ∧ treated_by(?g, ExternalBeamRadiotherapy)

# Stupp protocol: Surgery → Concurrent RT (60Gy) + TMZ (75 mg/m²) → Adjuvant TMZ (6 cycles)
```

**Rule 9: Vasospasm monitoring after SAH**

```swrl
# All SAH patients require nimodipine + TCD monitoring
SubarachnoidHemorrhage(?sah) ∧ has_etiology(?sah, AneurysmalSAH)
→ treated_by(?sah, Nimodipine_21days) ∧ requires(?sah, TCD_monitoring) ∧ has_vasospasm_risk(?sah, Peak_Day7)

# Nimodipine: 60 mg PO q4h × 21 days (mandatory, reduces DCI and poor outcome)
```

**Rule 10: Propagate anatomical relationships (transitivity)**

```swrl
# Transitivity of part_of relationship
part_of(?x, ?y) ∧ part_of(?y, ?z) → part_of(?x, ?z)

# Example: Hippocampus part_of MedialTemporalLobe part_of TemporalLobe
# Inference: Hippocampus part_of TemporalLobe
```

**Rule 11: Infer arterial supply from location**

```swrl
# Infer vascular territory from anatomical location
Pathology(?p) ∧ has_location(?p, ?anatLoc) ∧ supplied_by(?anatLoc, ?artery)
→ has_vascular_territory(?p, ?artery)

# Example: Lesion in Basal Ganglia → MCA_M1 lenticulostriate branches
# Used for stroke localization, surgical planning (preserving perforators)
```

---

### PROBABILISTIC REASONING (BAYESIAN NETWORKS) ⭐⭐:

**Network 1: Ring-enhancing lesion differential**

```bayesian
# Prior probabilities (adult patient, single lesion)
P(Glioblastoma) = 0.40
P(Metastasis) = 0.35
P(Abscess) = 0.15
P(SubacuteInfarct) = 0.10

# Likelihood ratios given imaging features
P(RingEnhancement | Glioblastoma) = 0.85
P(RestrictedDiffusion | Glioblastoma) = 0.10 # KEY: Low likelihood ⭐
P(ElevatedCBV | Glioblastoma) = 0.80

P(RingEnhancement | Abscess) = 0.90
P(RestrictedDiffusion | Abscess) = 0.95 # KEY: High likelihood ⭐
P(ElevatedCBV | Abscess) = 0.20

P(RingEnhancement | Metastasis) = 0.70
P(RestrictedDiffusion | Metastasis) = 0.05
P(MultipleMultipleLesions | Metastasis) = 0.60

# Posterior calculation (Bayes' theorem):
# IF RingEnhancement + RestrictedDiffusion observed:
# P(Abscess | RingEnh + RestrictedDiff) ≈ 0.75 ⭐ (high confidence)
# P(Glioblastoma | RingEnh + RestrictedDiff) ≈ 0.15
```

**Network 2: Aneurysm rupture risk prediction**

```bayesian
# PHASES score components (Population, Hypertension, Age, Size, Earlier SAH, Site)
# Conditional probabilities:

P(Rupture_5year | Size<7mm, NoHypertension, Age<70) = 0.02 # 2%
P(Rupture_5year | Size7-12mm, Hypertension, Age>70) = 0.15 # 15%
P(Rupture_5year | Size>12mm, Hypertension, Age>70, PriorSAH) = 0.40 # 40%

# Decision threshold: Treat if 5-year rupture risk >2-3% (balance treatment risk vs rupture risk)
# Coiling risk: Permanent morbidity 5-7%, mortality 1-2%
```

---

**CROSS-REFERENCES**:
- Anatomical entities → LEVEL3 anatomical specifications (complete mapping)
- Pathological entities → FUNDAMENTAL_NEUROSURGICAL_KNOWLEDGE_COMPLETE.md
- Imaging findings → LEVEL7_COMPLEX_NEUROANATOMICAL_IMAGE_ANALYSIS_COMPLETE.md
- Functional neuroanatomy → LEVEL3_FUNCTIONAL_NEUROANATOMY_COMPLETE.md
- White matter tracts → LEVEL3_WHITE_MATTER_TRACTS_COMPLETE.md
- Spine & spinal cord → LEVEL3_SPINE_SPINAL_CORD_COMPLETE.md
- Cranial nerves → LEVEL3_CRANIAL_NERVES_COMPLETE.md
- Skull base foramina → LEVEL3_SKULL_BASE_FORAMINA_COMPLETE.md
- Ventricular system → LEVEL3_VENTRICULAR_SYSTEM_COMPLETE.md
- Venous anatomy → LEVEL3_VENOUS_ANATOMY_COMPLETE.md

---

## IX. IMPLEMENTATION NOTES ⭐⭐

### KNOWLEDGE GRAPH STORAGE:

├─ **Triple store options**:
│   ├─ RDF databases: Apache Jena Fuseki, Blazegraph, Virtuoso
│   ├─ Property graph: Neo4j (with RDFS/OWL mapping layer)
│   └─ Hybrid: PostgreSQL + pgvector for embeddings, triple store for reasoning

├─ **Indexing strategy**:
│   ├─ Full-text search: Elasticsearch on entity labels, definitions, synonyms
│   ├─ Spatial indexing: PostGIS for anatomical location queries
│   └─ Graph traversal: Optimized for part_of, adjacent_to, tributary_of

└─ **Query optimization**:
    ├─ Materialized views: Pre-compute common query patterns
    ├─ Caching: Redis for frequent differential diagnosis queries
    └─ Batch reasoning: Run OWL inference offline, cache results

---

### ONTOLOGY VERSIONING:

├─ **Version control**:
│   ├─ Git repository for OWL/RDF files
│   ├─ Semantic versioning: MAJOR.MINOR.PATCH
│   └─ Migration scripts for schema changes

├─ **Update triggers**:
│   ├─ New WHO classification: Major version increment
│   ├─ New clinical trial data: Minor version increment
│   └─ Bug fixes, clarifications: Patch version increment

└─ **Backward compatibility**:
    ├─ Deprecate classes/properties with owl:deprecated
    └─ Maintain aliases for renamed entities

---

### RAG INTEGRATION:

├─ **Embedding generation**:
│   ├─ Entity embeddings: Train on ontology structure + clinical text
│   ├─ Relationship embeddings: TransE, RotatE for knowledge graph completion
│   └─ Multi-modal: Image embeddings (CT/MRI) aligned with ontology entities

├─ **Retrieval strategies**:
│   ├─ Hybrid search: Dense (embedding similarity) + Sparse (keyword BM25)
│   ├─ Graph-constrained retrieval: Expand query along relationship paths
│   └─ Contextual re-ranking: Use ontology constraints to filter results

└─ **Query augmentation**:
    ├─ Expand query with synonyms (has_synonym property)
    ├─ Include superclasses (via part_of, IS-A hierarchy)
    └─ Related entities (via adjacent_to, associated_with)

---

## X. SUMMARY STATISTICS ⭐⭐⭐

### ONTOLOGY COMPLETENESS:

**Entity Taxonomy (TBox)**:
- Total entity classes: 800+ entities across all domains
- AnatomicalEntity: 450+ structures (CNS, PNS, vascular, skull, spine)
- PathologicalEntity: 150+ diseases (neoplasms, vascular, degenerative, trauma, infections)
- ClinicalFinding: 80+ signs and symptoms
- Intervention: 60+ surgical procedures, radiation, chemotherapy, medical management
- DiagnosticTest: 40+ imaging modalities, laboratory tests, electrophysiology
- Outcome: 20+ clinical outcomes, tumor response, complications

**Relationship Types (Object Properties)**:
- Total relationships: 30+ relationship types
- Anatomical: part_of, regional_part_of, tributary_of, continuous_with, adjacent_to, supplies, drains_into
- Pathological: has_location, causes, associated_with, progresses_to, has_molecular_feature
- Clinical: has_symptom, has_sign, has_imaging_finding, diagnosed_by, treated_by
- Intervention: targets, has_complication, requires, achieves
- Diagnostic: detects, reveals

**Attribute Schemas (Data Properties)**:
- Total attributes: 40+ data properties
- General: has_name, has_synonym, has_definition, has_FMA_ID, has_SNOMED_CT_ID, has_RadLex_ID
- Anatomical: has_laterality, has_brodmann_area, has_spinal_level, has_vessel_segment
- Pathology: has_WHO_grade, has_IDH_status, has_MGMT_status, has_1p19q_status, has_size_mm, has_GCS_score
- Imaging: has_HU_value, has_T1_signal, has_T2_signal, has_ADC_value, has_CBV_value, has_FA_value, has_ASPECTS_score
- Treatment: has_extent_of_resection, has_radiation_dose_Gy, has_DBS_target, has_surgical_approach
- Outcome: has_median_survival_months, has_KPS_score, has_mRS_score, has_complication_rate_percent

**Query Patterns**:
- Differential diagnosis queries: 3 comprehensive patterns
- Treatment selection queries: 2 decision-tree algorithms
- Prognosis prediction queries: 2 multivariable models
- Complication risk queries: 1 risk stratification framework

**Temporal Relationships**:
- Disease progression timelines: 4 sequences (glioma, oligodendroglioma, aneurysm, disc herniation, stroke)
- Treatment sequencing protocols: 4 algorithms (GBM Stupp, metastasis, SAH, disc herniation)

**Probabilistic Relationships**:
- Risk factors: 4 categories (brain tumors, aneurysms, stroke, disc herniation) with odds ratios, relative risks
- Prognostic factors: 4 diseases (GBM, SAH, stroke, meningioma) with hazard ratios, survival probabilities

**Reasoning Rules**:
- OWL axioms: 5 rules (tumor classification, diagnostic criteria, imaging differential, surgical urgency, treatment selection)
- SWRL rules: 6 rules (eloquent cortex, thrombolysis eligibility, treatment protocol, vasospasm monitoring, transitivity, vascular territory)
- Bayesian networks: 2 networks (differential diagnosis, rupture risk prediction)

**Standard Ontology Mappings**:
- FMA (Foundational Model of Anatomy): 450+ anatomical entity mappings
- SNOMED CT: 200+ clinical concept mappings
- RadLex: 80+ imaging finding mappings
- Gene Ontology (GO): 20+ molecular pathway mappings
- Human Phenotype Ontology (HPO): 40+ phenotype mappings
- NCIt (National Cancer Institute Thesaurus): 30+ neuro-oncology concept mappings

---

### CLINICAL COVERAGE:

**Neurosurgical Subspecialties**:
- Neuro-oncology: ⭐⭐⭐ Comprehensive (primary brain tumors, metastases, molecular genetics, treatment protocols)
- Cerebrovascular: ⭐⭐⭐ Comprehensive (aneurysms, AVMs, dAVF, cavernomas, stroke, hemorrhage)
- Spine: ⭐⭐⭐ Comprehensive (degenerative disease, trauma, tumors, infections)
- Functional: ⭐⭐ Moderate (DBS, epilepsy surgery, pain management)
- Trauma: ⭐⭐ Moderate (TBI, SCI, ICP management, decompressive craniectomy)
- Pediatric: ⭐ Basic (medulloblastoma, ependymoma, neural tube defects, Chiari malformations)
- Skull base: ⭐⭐ Moderate (pituitary adenomas, craniopharyngioma, acoustic neuroma)

**Evidence-Based Medicine Integration**:
- Clinical trials referenced: 15+ landmark trials (Stupp, ISAT, SPORT, RESCUEicp, DAWN, DEFUSE-3)
- Grading systems: 20+ scoring systems (WHO, Hunt-Hess, WFNS, Fisher, Simpson, Spetzler-Martin, GPA, PHASES)
- Treatment guidelines: 10+ protocols (Stupp, SAH management, acute stroke, TBI)
- Epidemiological data: 100+ statistics (incidence, survival, complication rates, risk factors with ORs/HRs)

---

### KNOWLEDGE GRAPH METRICS:

**Estimated triple count** (when fully instantiated):
- TBox (schema): ~5,000 triples (entity classes, relationships, constraints)
- ABox (instances, will grow with clinical cases): Scalable to millions of patient-specific triples

**Reasoning complexity**:
- Description Logic expressivity: SROIQ(D) (OWL 2 DL)
- Decidable: Yes
- Reasoning time: O(n²) for classification, O(n) for consistency checking (n = entities)
- Scalability: Suitable for clinical decision support with caching and materialized views

**Interoperability**:
- RDF/OWL standard compliance: Full
- SPARQL query support: Full
- REST API exposure: Planned (via GraphQL or SPARQL endpoint)
- FHIR integration: Possible via SNOMED CT/ICD-10 mappings

---

**TOTAL LINE COUNT**: 2,277 lines of ultra-granular medical ontology specification

**KNOWLEDGE DOMAIN COVERAGE**: Comprehensive neurosurgical knowledge graph architecture spanning anatomy, pathology, imaging, clinical findings, interventions, outcomes, temporal/probabilistic relationships, and reasoning rules for surgical planning and clinical decision support.

**IMPLEMENTATION READINESS**: Production-ready specification for OWL 2 DL ontology implementation with triple store backend, SPARQL query interface, RAG integration, and clinical decision support system deployment.
