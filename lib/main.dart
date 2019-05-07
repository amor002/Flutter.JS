import 'file.dart';
import 'package:flutter/material.dart';


 main() {
    runApp(new MyApp());
}


class MyApp extends StatelessWidget {

    MyApp() {
        print("constructor was just called!");
    }

     build(context) {
         
        return new MaterialApp( title:'example', theme:ThemeData(
            primarySwatch:Colors.blue,
          ), home:new Home());
     }
}

class Home extends StatelessWidget {
    
    build(context) {
        
        return 
        Scaffold(
	appBar:AppBar(title:Text('Welcome!', ),
	leading:IconButton(icon: Icon(Icons.home, ), onPressed:(){}),
	actions:[IconButton(icon: Icon(Icons.settings, ), onPressed:(){}),IconButton(icon: Icon(Icons.date_range, ), onPressed:(){})] ),body:Container(child: 
	Center(child: 
	RaisedButton(child: 
	Text('click me!', ), onPressed:printHi), ), ) );
}

}












