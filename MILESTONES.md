# Milestone 1
### Discussions on Ideas
#### Candidate ideas
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
### Brief Description of Your Planned Program Analysis (& Visualisation, if Applicable) Ideas
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
### Follow-up Tasks/Features Still to Design
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

# Milestone 3
### Visual Mockup
#### Note: Design Not Final
![](https://media.github.students.cs.ubc.ca/user/1447/files/98252200-43fd-11ec-8340-cf71c1ba500d)
### User Study
#### Question 1 </br>
Describe how the type of var changes with the code’s execution. Perform type analysis on the variable var when the code executes line 8.  </br>

    1    var = 10
    2    rand_bool = 0 or 1 or 2 uniform random 
    3    if (rand_bool == 2):
    4        var = “abc”
    5    elif (rand_bool == 1):
    6        var = [1, 2, 3]
    7    else:
    8        var += 5
    9    print(var)
##### Solution: </br>
Var: </br>
rand_bool == 0, 1/3 probability, int from start to finish</br>
rand_bool == 1, 1/3 probability, int @ line 1 -> array @ line 6 to finish</br>
rand_bool == 2, 1/3 probability, int @ line 1 -> string @ line 4 to finish</br>
At line 9, var could be either an int, string, or array each with 1/3 probability.</br>

#### Question 2</br>
Perform type analysis on the variables a, b, and c. Consider both the error and valid cases. Draw clues from the implementation. For the purposes of this exercise, consider only the following types: int, float, boolean, string, list, tuple, dictionary, and set.</br>

    1    c = a + b.split(“.”)
##### Solution:</br>
Error case: b is not a string. Error thrown.</br>
Error case: a is not an array/list. Error thrown.</br>
Valid case: split only works on string inputs, thus b must be a string. b.split(“.”) will separate the string b by “.” and return a list. Addition only works when both sides are arrays, thus variable a must also be an array. Since a and b.split are both arrays, c must also be an array.</br>

#### Question 3</br>
Perform type analysis on the variables in the function foo(a, b). Consider both the error and valid cases. Draw clues from the implementation. For the purposes of this exercise, consider only the following types: int, float, boolean, string, list, tuple, dictionary, and set.</br>

    1    def foo(a, b):
    2        c = a[0] + b[0]
    3        print(c)
    4    def main():
    5        a = ??? <-- unknown
    6        b = ??? <-- unknown
    7        foo(a, b)
##### Solution:</br>
Both variables, a and b, undergo index accesses, then they must be either one of list, string, tuple, dictionary with keys of 0. For a[0] + b[0] to work, both terms are likely the same type. String + string, int/float/bool + int/float/bool, list + list, or tuple + tuple. Thus, c could be either a string, int, float, boolean, list, or tuple.</br>


#### Question 4</br>
After doing type analysis by hand, do you feel that a tool for performing type analysis automatically would be beneficial to python programmers? Any features you would like to see or use in a type analysis tool? </br>

### User Study Results
##### Question 1
- The user had to consider the possible values for the random boolean to analyze each branch of the if-statement to infer the possible types for var at line 9.
- The user correctly answered that it can be any of the three types with probability 1/3.
##### Question 2
- The user had no problem with identifying the types for variables a, b, c. 
- Also identified the possible error cases if b is not the correct type for splitting and when a is not the correct type for the addition operator.
##### Question 3
- The user correctly identified int, float, boolean cannot be possible answers.
- The user was not really familiar with how some types can be accessed with the bracket notation, such as when the variable is a dictionary or a set.
-The user had to manually consider the different combinations of a[0] and b[0] to infer the possible type of c.
##### Question 4
- The user thought that a tool which could do this automatically would be very helpful. The user is more familiar with matlab, so the user compares some type errors that occur in python and matlab.
##### Reflection about the user study
- It can be very tedious for a user to have to step through all lines of code to identify the possible type of one variable. Especially if we were to analyze large blocks of code, it would not be an easy task. Particularly, this task can become very difficult for inexperienced programmers, which is our target audience, so a tool to automatically execute a static type analysis should be very helpful as observed in the responses from our user study.


### Changes to Original Design
- Added features for error checking, such as type mismatch, faulty function parameters, etc. Decreased emphasis on the visualization component. Increased emphasis on the analysis component.
### Planned Timeline
- 11/19 Plan final user study and start considering participants
- 11/18 or 11/19 Finish implementing the static analysis portion of the project
- 11/23 or 11/24 Finish implementing the visual component 
- 11/25 or 11/26 Create the video for the project
### TA Feedback
- Should include type inference in function calls, such as when parameters are passed in, but we don’t have their types explicitly defined.
- Start thinking about actual use cases with complex examples for the static analysis. 
- No need to focus too much on visualization. 
- Try a branching flow chart instead of a scatter plot for the type history diagram.

