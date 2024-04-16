import os

# Utworzenie wymaganych katalogów dla plików kontrolnych
os.mkdir('system')
os.mkdir('constant')
os.mkdir('0')


# Zdefiniowanie wartości symulacji

startTime = 0
endTime = 2000
writeInterval = 50

# Utworzenie zmiennych i nadanie im wartości wymaganych do plików kontrolnych
dataControlDict = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      controlDict;
}

application         buoyantSimpleFoam;
startFrom           startTime;
startTime           """+str(startTime)+""";
stopAt              endTime;
endTime             """+str(endTime)+""";
deltaT              1;
writeControl        timeStep;
writeInterval       """+str(writeInterval)+""";
purgeWrite          0;
writeFormat         ascii;
writePrecision      6;
writeCompression    off;
timeFormat          general;
"""

dataBlockMeshDict = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}

scale   0.001;

vertices
(
    ( 0     0   -50)
    (100    0   -50)
    (100  500   -50)
    ( 0   500   -50)
    ( 0     0    50)
    (100    0    50)
    (100  500    50)
    ( 0   500    50)
);
edges
(
);
blocks
(
    hex (0 1 2 3 4 5 6 7) (35 150 15) simpleGrading (1 1 1)
);

boundary
(
    frontAndBack
    {
        type wall;
        faces
        (
            (0 1 5 4)
            (2 3 7 6)
        );
    }

    topAndBottom
    {
        type wall;
        faces
        (
            (4 5 6 7)
            (3 2 1 0)
        );
    }

    hot
    {
        type wall;
        faces
        (
            (6 5 1 2)
        );
    }

    cold
    {
        type wall;
        faces
        (
            (4 7 3 0)
        );
    }
);
mergePatchPairs
(
);
"""

dataFvSchemes = """

FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      fvSchemes;
}

ddtSchemes
{
    default steadyState;
}

gradSchemes
{
    default         Gauss linear;
}

divSchemes
{
    default         none;

    div(phi,U)      bounded Gauss limitedLinear 0.2;

    energy          bounded Gauss limitedLinear 0.2;
    div(phi,K)      $energy;
    div(phi,h)      $energy;

    turbulence      bounded Gauss limitedLinear 0.2;
    div(phi,k)      $turbulence;
    div(phi,epsilon) $turbulence;
    div(phi,omega) $turbulence;

    div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;
}

laplacianSchemes
{
    default         Gauss linear orthogonal;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         orthogonal;
}

wallDist
{
    method          meshWave;
}

"""

dataFvSolution = """

FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      fvSolution;
}

solvers
{
    p_rgh
    {
        solver           GAMG;
        tolerance        1e-7;
        relTol           0.01;
        smoother         DICGaussSeidel;
    }

    "(U|h|k|epsilon|omega)"
    {
        solver          PBiCGStab;
        preconditioner  DILU;
        tolerance       1e-8;
        relTol          0.1;
    }
}

SIMPLE
{
    momentumPredictor no;
    nNonOrthogonalCorrectors 0;
    pRefCell        0;
    pRefValue       0;

    residualControl
    {
        p_rgh           1e-4;
        U               1e-4;
        h               1e-4;

        // possibly check turbulence fields
        "(k|epsilon|omega)" 1e-3;
    }
}

relaxationFactors
{
    fields
    {
        rho             1.0;
        p_rgh           0.7;
    }
    equations
    {
        U               0.3;
        h               0.3;
        "(k|epsilon|omega)" 0.7;
    }
}

"""

dataG = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       uniformDimensionedVectorField;
    object      g;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 1 -2 0 0 0 0];
value           (0 -9.81 0);
"""

dataThermophysicalProperties = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      thermophysicalProperties;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

thermoType
{
    type            heRhoThermo;
    mixture         pureMixture;
    transport       const;
    thermo          hConst;
    equationOfState perfectGas;
    specie          specie;
    energy          sensibleEnthalpy;
}

mixture
{
    specie
    {
        molWeight       28.96;
    }
    thermodynamics
    {
        Cp              1004.4;
        Hf              0;
    }
    transport
    {
        mu              1.831e-05;
        Pr              0.705;
    }
}
"""

dataTurbulenceProperties = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      turbulenceProperties;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

simulationType          RAS;

RAS
{
    RASModel            kOmegaSST;

    turbulence          on;

    printCoeffs         on;
}
"""

dataT = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      T;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 1 0 0 0];

internalField   uniform 293;

boundaryField
{
    frontAndBack
    {
        type            zeroGradient;
    }

    topAndBottom
    {
        type            zeroGradient;
    }

    hot
    {
        type            fixedValue;
        value           uniform 343.15; // 70 degC
    }

    cold
    {
        type            fixedGradient;
        gradient        uniform 100; // 
    }
}
"""

dataU = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       volVectorField;
    object      U;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 1 -1 0 0 0 0];

internalField   uniform (0 0 0);

boundaryField
{
    frontAndBack
    {
        type            noSlip;
    }

    topAndBottom
    {
        type            noSlip;
    }

    hot
    {
        type            noSlip;
    }

    cold
    {
        type            noSlip;
    }
}
"""

dataPrgh = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      p_rgh;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [1 -1 -2 0 0 0 0];

internalField   uniform 1e5;

boundaryField
{
    frontAndBack
    {
        type            fixedFluxPressure;
        value           uniform 1e5;
    }

    topAndBottom
    {
        type            fixedFluxPressure;
        value           uniform 1e5;
    }

    hot
    {
        type            fixedFluxPressure;
        value           uniform 1e5;
    }

    cold
    {
        type            fixedFluxPressure;
        value           uniform 1e5;
    }
}
"""

dataP = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      p;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [1 -1 -2 0 0 0 0];

internalField   uniform 1e5;

boundaryField
{
    frontAndBack
    {
        type            calculated;
        value           $internalField;
    }

    topAndBottom
    {
        type            calculated;
        value           $internalField;
    }

    hot
    {
        type            calculated;
        value           $internalField;
    }

    cold
    {
        type            calculated;
        value           $internalField;
    }
}
"""

dataOmega = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      omega;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 -1 0 0 0 0];

internalField   uniform 0.12;

boundaryField
{
    frontAndBack
    {
        type            omegaWallFunction;
        value           uniform 0.12;
    }

    topAndBottom
    {
        type            omegaWallFunction;
        value           uniform 0.12;
    }

    hot
    {
        type            omegaWallFunction;
        value           uniform 0.12;
    }

    cold
    {
        type            omegaWallFunction;
        value           uniform 0.12;
    }
}
"""

dataNut = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      nut;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 2 -1 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    frontAndBack
    {
        type            nutUWallFunction;
        value           uniform 0;
    }

    topAndBottom
    {
        type            nutUWallFunction;
        value           uniform 0;
    }

    hot
    {
        type            nutUWallFunction;
        value           uniform 0;
    }

    cold
    {
        type            nutUWallFunction;
        value           uniform 0;
    }
}
"""

dataK = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      k;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 2 -2 0 0 0 0];

internalField   uniform 3.75e-04;

boundaryField
{
    frontAndBack
    {
        type            kqRWallFunction;
        value           uniform 3.75e-04;
    }

    topAndBottom
    {
        type            kqRWallFunction;
        value           uniform 3.75e-04;
    }

    hot
    {
        type            kqRWallFunction;
        value           uniform 3.75e-04;
    }

    cold
    {
        type            kqRWallFunction;
        value           uniform 3.75e-04;
    }
}
"""

dataEpsilon = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      epsilon;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 2 -3 0 0 0 0];

internalField   uniform 4e-06;

boundaryField
{
    frontAndBack
    {
        type            epsilonWallFunction;
        value           uniform 4e-06;
    }

    topAndBottom
    {
        type            epsilonWallFunction;
        value           uniform 4e-06;
    }

    hot
    {
        type            epsilonWallFunction;
        value           uniform 4e-06;
    }

    cold
    {
        type            epsilonWallFunction;
        value           uniform 4e-06;
    }
}
"""

dataAlphaT = """
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      alphat;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [1 -1 -1 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    frontAndBack
    {
        type            compressible::alphatWallFunction;
        Prt             0.85;
        value           uniform 0;
    }

    topAndBottom
    {
        type            compressible::alphatWallFunction;
        Prt             0.85;
        value           uniform 0;
    }

    hot
    {
        type            compressible::alphatWallFunction;
        Prt             0.85;
        value           uniform 0;
    }

    cold
    {
        type            compressible::alphatWallFunction;
        Prt             0.85;
        value           uniform 0;
    }
}
"""



#Utworzenie i zapis zmiennych do plików kontrolnych

with open("system/controlDict", "w") as file:
    file.write(dataControlDict)

with open("system/blockMeshDict", "w") as file:
    file.write(dataBlockMeshDict)

with open("system/fvSchemes", "w") as file:
    file.write(dataFvSchemes)

with open("system/fvSolution", "w") as file:
    file.write(dataFvSolution)

with open("constant/g", "w") as file:
    file.write(dataG)

with open("constant/thermophysicalProperties", "w") as file:
    file.write(dataThermophysicalProperties)

with open("constant/turbulenceProperties", "w") as file:
    file.write(dataTurbulenceProperties)

with open("0/T", "w") as file:
    file.write(dataT)

with open("0/U", "w") as file:
    file.write(dataU)

with open("0/p_rgh", "w") as file:
    file.write(dataPrgh)

with open("0/p", "w") as file:
    file.write(dataP)

with open("0/omega", "w") as file:
    file.write(dataOmega)

with open("0/nut", "w") as file:
    file.write(dataNut)

with open("0/k", "w") as file:
    file.write(dataK)

with open("0/epsilon", "w") as file:
    file.write(dataEpsilon)

with open("0/alphat", "w") as file:
    file.write(dataAlphaT)