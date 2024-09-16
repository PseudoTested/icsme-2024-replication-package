# ICSME 2024: Exploring Pseudo-Testedness - Replication Package

This repository contains a replication package for the paper

```
M. Maton, G. M. Kapfhammer, and P. McMinn. Exploring pseudo-testedness: Empirically evaluating extreme mutation testing at the statement level. In Proc. ICSME, 2024.
```

This includes the following:

- `projects.md` - Information on the projects used in the study
- `output-data/` - Data collected during original experiments
- `extract-data/` - Scripts used to extract relevant data
- `project-characterisation.ipynb` - Jupyter notebook to characterise projects
- `RQ1.ipynb` - Jupyter notebook to extract and present data to answer RQ1.
- `RQ2and3.ipynb` - Jupyter notebook to extract and present data to answer RQs 2
  and 3. 

## PseudoSweep

To build `PseudoSweep`, see the [PseudoSweep GitHub
Repository](https://github.com/PseudoTested/PseudoSweep) for instructions. The
`.jar` file produced after building the project is required for running the
experiments.

### Operators

The operators used in PseudoSweep are listed below, with further details in the
tool demonstration paper: `PSEUDOSWEEP: A Pseudo-Tested Code Identifier`.

| Operator | Description                                   |
| -------- | --------------------------------------------- |
| MDR      | Delete method body and return default value   |
| MDV      | Delete method body                            |
| SDSS     | Delete statement                              |
| SDSL     | Delete statement with label                   |
| SDSR     | Delete the statement and return default value |
| SDVD     | Delete declaration initialisation             |
| SFCT     | Fix conditional expression to True            |
| SDLL     | Delete loop statement with label              |

Where operators require default return values, they are as follows:

| Type           | Default Values             |
| -------------- | -------------------------- |
| Boolean        | false, true                |
| Byte           | 0, 1                       |
| Double         | 0, 1                       |
| Float          | 0, 1                       |
| Char           | \40 (space character), 'A' |
| Short          | 0, 1                       |
| Int            | 0, 1                       |
| String         | "", "A"                    |
| Long           | 0, 1                       |
| Collection     | null, new ArrayList        |
| Iterable       | null, new ArrayList        |
| List           | null, new ArrayList        |
| Queue          | null, new LinkedList       |
| Set            | null, new HashSet          |
| Map            | null, new HashMap          |
| Reference Type | null, null                 |

## Running data collection scripts

See the [PseudoSweep Demo
Repo](https://github.com/PseudoTested/pseudosweep-demo) for a single project
setup example. The `run-pseudosweep.sh` script produces the statement and method
level outputs used in results. 

We also ran the `PIT` mutation tool on each project using the Gregor Mutation Engine and the Default
mutant operator set. 

## Test Exclusion
In order to run `PseudoSweep` we had to exclude some tests within our subjects
from consideration. This may have lead to some inaccuracies in our results.

Such tests include tests that start threads within the tests themselves and some
parameterized tests. `PseudoSweep` currently ignores parameterized tests.


## Running Data analysis scripts
The `read-projects.py` script collates all the data from each project into a
model and produces summary `.csv` files. These `.csv` files summarise the data of
full projects, methods, and statements as well as locating the mutants placed in
each of these by `PIT`. 

## Using the results
This data is then read by `.ipynb` files to characterise the projects and
analyse the data in order to answer the questions. This includes producing the
the figures and table data used in the paper. 

See each directory for further information.
