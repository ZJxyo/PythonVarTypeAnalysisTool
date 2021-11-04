# Milestone 1
### Discussions on Ideas
#### Candidate Ideas
- Control flow visualization. Mapping logical paths into a tree for visualization
- Linter for syntax and type checking. Highlighting & statistics for visualization
- Stack visualization
- Hierarchy visualization (of superclass, interfaces, etc.), similar to UML diagrams
#### Discussions
- By defining the problem statement and target audience, we can easily limit the complexity, length, and scope of the intended input program of our analysis tool. For example, we could argue that the control flow visualization tool is meant for providing visual aid of the execution process to entry level or beginner programmers. The assumption of short and simple inputs should address control flow visualization’s complexity problem.

### TA Feedback
- Control flow can get overly complex when analyzing the entire program
- Recommended to perform analyses on a subset of the program, such as methods
- Analyze a subset of the programming language to avoid complex processes such as dynamic dispatch and reflection
- Focus on the visualization if program analysis is lacking

### Follow-up Tasks
- Decide on which programming language to focus on
- Pick the idea to implement
- Sketch out the process of our analysis idea
- Flesh out the details of ideas, finalize the appropriate subset of the programming language we choose
- Design details and features

# Milestone 2
### Brief description of your planned program analysis (and visualisation, if applicable) ideas
#### Problem statement
Static program analysis of variable types in a Python program.
#### Features
Visualization includes: statistics; graphs, such as a pie chart showing type distribution; Color coding different types in the code; The analysis shall be performed globally and on a per-variable basis. The type history of each variable name should be recorded. Globally, the total distribution of types could be analyzed as statistics. For example, we could present a count of the total number of types, total number of variables with ambiguous types, and the total number of type changes in a given program.
#### Target audience
Entry level python users whose programs are not overly complex and involve only a set of popular python libraries, such as NumPy. Custom classes should be allowed as well. The input program should contain operations that result in a variable conditionally changing types during program execution. Type consistency could also be used as a measure for code quality.
#### Visualization samples (mockup)
![](p2mockup1.PNG)
### TA Feedback
- Static analysis would be ideal for this project idea, as performing dynamic analysis would be as simple as inserting code to wherever the variable type is ambiguous.
- Project should include non-trivial analysis, such as inferring, approximating, and estimating information. 
### Follow-up tasks/features still to design
- Consider type casting and its effects
- Consider linting?
- Investigate libraries for parsing the source code
- Narrow down the set of python libraries to analyze
- Learn more about usable visualization tools
### Division of Tasks
To be determined once the project starts to take shape. Meanwhile, all tasks are to be handled as a group activity.
### Roadmap 
- Design user study
- Find participant
- Think of more features
- Start implementation

