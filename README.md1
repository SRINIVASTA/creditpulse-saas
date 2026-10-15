graph TD
    %% Tooltips and Styles
    classDef roots fill:#f9f,stroke:#333,stroke-width:2px;
    classDef trunk fill:#bbf,stroke:#333,stroke-width:2px;
    classDef leaves fill:#bfb,stroke:#333,stroke-width:2px;

    %% --- STAGE 1: THE ROOTS (Design & Machinery) ---
    subgraph Stage_1 [Stage 1: Foundational Roots]
        EDA[<b>EDA Companies</b><br>• Synopsys, Cadence<br>• Provides design software]
        IP[<b>IP & Design Service</b><br>• ARM, Imagination<br>• Provides core blueprints]
        Equip[<b>Fab Equipment & Materials</b><br>• ASML, Applied Materials<br>• Provides manufacturing machines]
    end

    %% --- STAGE 2: THE TRUNK (Manufacturing) ---
    subgraph Stage_2 [Stage 2: Core Processing]
        Foundry[<b>Foundries / IDMs</b><br>• TSMC, Intel, Samsung<br>• Prints designs onto silicon wafers]
    end

    %% --- STAGE 3: THE FINISHING (Packaging & Test) ---
    subgraph Stage_3 [Stage 3: Assembly & Validation]
        OSAT[<b>Test & OSAT Companies</b><br>• Amkor, ASE, Teradyne<br>• Cuts, packages, and tests chips]
    end

    %% --- STAGE 4: THE BRANCHES (Final Products) ---
    subgraph Stage_4 [Stage 4: Specialized Final Chips]
        Fabless[<b>Fabless Market</b><br>• NVIDIA, Qualcomm, AMD]
        Analog[<b>Analog & Mixed Signal</b><br>• ADI, onsemi]
        Memory[<b>Memory Chips</b><br>• SK hynix, Micron]
        Auto[<b>Automotive Semiconductor</b><br>• Bosch, Renesas]
        Startups[<b>Emerging Startups</b><br>• InCore, Saankhya]
    end

    %% Tree Connections
    EDA --> Foundry
    IP --> Foundry
    Equip --> Foundry
    
    Foundry --> OSAT
    
    OSAT --> Fabless
    OSAT --> Analog
    OSAT --> Memory
    OSAT --> Auto
    OSAT --> Startups

    %% Apply Styles
    class EDA,IP,Equip roots;
    class Foundry,OSAT trunk;
    class Fabless,Analog,Memory,Auto,Startups leaves;
