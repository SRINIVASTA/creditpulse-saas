graph TD
    %% STAGE 1: FOUNDATIONAL ROOTS
    subgraph Stage_1_Roots [Stage 1: Foundational Roots]
        EDA[EDA Software - Synopsys, Cadence]
        IP[IP Blueprints - ARM, Imagination]
        Equip[Fab Equipment - ASML, Lam Research]
    end

    %% STAGE 2: MANUFACTURING TRUNK
    subgraph Stage_2_Trunk [Stage 2: Processing Trunk]
        Foundry[Foundries and IDMs - TSMC, Intel, Samsung]
    end

    %% STAGE 3: FINISHING STAGE
    subgraph Stage_3_Finish [Stage 3: Assembly and Validation]
        OSAT[Test and OSAT Companies - Amkor, ASE]
    end

    %% STAGE 4: THE BRANCHES
    subgraph Stage_4_Branches [Stage 4: Specialized Final Chips]
        Fabless[Fabless Market - NVIDIA, Qualcomm]
        Analog[Analog and Mixed Signal - ADI, onsemi]
        Memory[Memory Chips - Micron, SK Hynix]
        Auto[Automotive Semi - Bosch, Renesas]
        Startups[Emerging Startups - InCore, Saankhya]
    end

    %% Tree Pipeline Connections
    EDA --> Foundry
    IP --> Foundry
    Equip --> Foundry
    
    Foundry --> OSAT
    
    OSAT --> Fabless
    OSAT --> Analog
    OSAT --> Memory
    OSAT --> Auto
    OSAT --> Startups
