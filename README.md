# Flutter JS (amr)
this python file allows you to build [flutter](https://flutter.io/) apps
using javascript and react but without the full access for both javascript and react
- means that javascript and react syntax will be stricted to a limit
- you will have a full access to all **dart** and **flutter** lib and syntax from **javascript** but not have full access to all **javascript** and **react** lib and syntax

#how it works:
the python script `amr.py` converts the javascript code into dart code, as much as possible, you can also improve the parser by your self if you want.

# how to start ?
1. first of all you must have flutter installed
2. create a flutter project using the command `flutter create <directory name>`
3. create a directory in the project and name it `javascript`
4. put the converter(`amr.py`) in the project directory

now you are ready to start using **Flutter JS**

## next:
1. inside `javascript` directory create file called `main.js` (required)
2. write the starting code in javascript
```javascript
import 'package:flutter/material.js';


function main() {
    runApp(new MyApp());
}


class MyApp extends StatelessWidget {

     build(context) {
         
        return new MaterialApp( title= 'example', theme=ThemeData(
            primarySwatch= Colors.blue,
          ), home= new Home()); //argument assign is required here
     }
}

class Home extends StatelessWidget {
    
    build(context) {

        return 
        <Scaffold>
            <appBar centerTitle={true}>
                <title>
                    <Text>Welcome!</Text>
                </title>
            </appBar>

            <body>
                <Container>
                    <Center>
                            <Text style={new TextStyle(fontSize=20.0)}>hello world!</Text>
                    </Center>
                </Container>
            </body>
        </Scaffold>;
}

}
```
3. open your emulator
4. run and check `python amr.py --run` (`--run` flag to build and run)

## how to use ?
* if need to import another js file just go ahead and import it `import 'file.js'`
* you may need to use dart libraries you can import it easly, example `import 'dart:math'`
* you can use the react tags any where but with rules
   * you can't use self closed tags without having a parent, example
          
	  ```javascript
		var txt = "hello!";
		let x = <Text value={txt}/>; // error
		// closed tag should always be inside another component
		// you can use this instead
		let x = <Text value={txt}></Text>; //works !   
          ```
##### functions as properties
* to pass a function as a property in react
	```javascript
	<RaisedButton onPressed={function() {
	// this is a mistake !
	// this will make the parser freezes while converting js to dart
	}}>
		...
	</RaisedButton>
	
	```
	* you can do it in two ways
		1. writing the function in one line
		2. declaring a function before using react, and using it as a property
			```javascript
			function doSomeThing() {
			 ...
			}
			
			<RaisedButton onPressed={doSomeThing}>
				...
			</RaisedButton>
			
			```

##### `value` property in components
this property allows you to insert values to some components that don't have optional argument in flutter
* example
		```java
			//dart code
			Text text = new Text(<value>);
			Image.network(<value>);
			...etc
          	```

##### available javascript differences
* **the supported javascript syntax which is not in dart that you are able to use**
* `setTimeout` built in function
* `function` keyword
* `let` keyword
* `instanceof` keyword
* `NaN`
* `parseInt` built in function
* `parseFloat` built in function
* `===`
* `console.log`
* `typeof` keyword
* `async` async functions
* `super`
* `constructor`
* default arguments
* adding object to a string,ex: `let x = "hello " + 1`
and you can add you own edition if needed

##### javascript blocked syntax

* object
    * you can't use `.` to access a propery, instead you can use
        ```javascript
            const x = {'name': 'amr elmowaled', 'country': 'egypt'};
            console.log(x.name); // error
            console.log(x['name']) // works
        ```
    * you can't use different types of values in the same object
        ```javascript
        var x = {'name': 'amr elmowaled', 'age': 17}; //error
        var x = {'name': 'amr elmowaled', 'numbers': {'age': 17}}; //works
        ```
    * you can't assign object value with an undefiened key
        ```javascript
        var x = {name: 'amr elmowaled'}; // error
        var x = {'name': 'amr elmowaled'} // work, string key is not neccessary you can use any other types
        ```
    * you can't add a property using `.`
        ```javascript

        x.name = 'amr elmowaled'; //error
        x['name'] = 'amr elmowaled'; //work
        ```

* you can't use any non-mentioned available javascript avaiable differences

* you are not allowed to define a new class instance variable that wasn't defined
    ```javascript

    class Car {

        constructor(color) {
            this.color = color; // error
        }
    }
    // you should define the property firstly
    class Car {

        var color;

        constructor(color) {
            this.color = color; // works!
        }
    }
    ```


* `this` keyword can only be used inside a class

# **Elmowaled Dev.**
