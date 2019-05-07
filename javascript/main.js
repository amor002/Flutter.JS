import 'file.js';
import 'package:flutter/material.js';


function main() {
    runApp(new MyApp());
}


class MyApp extends StatelessWidget {

    constructor() {
        console.log("constructor was just called!");
    }

     build(context) {
         
        return new MaterialApp( title= 'example', theme=ThemeData(
            primarySwatch= Colors.blue,
          ), home= new Home());
     }
}



class Home extends StatelessWidget {
    
    build(context) {

        let style = <TextStyle color={Colors.blue}></TextStyle>;

        return 
        <Scaffold>
            <appBar>
                <title>
                    <Text>Welcome!</Text>
                </title>
                <leading>
                    <IconButton onPressed={function(){}}>
                        <Icon value={Icons.home}/>
                    </IconButton>
                </leading>
                <actions>
                    <IconButton onPressed={function(){}}>
                            <Icon value={Icons.settings}/>
                    </IconButton>
                    <IconButton onPressed={function(){}}>
                        <Icon value={Icons.date_range}/>
                    </IconButton>
                </actions>
            </appBar>

            <body>
                <Container>
                    <Center>
                            <FlatButton onPressed={printHi}>
                                <Text style={style}>click me!</Text>
                            </FlatButton>
                    </Center>
                </Container>
            </body>
        </Scaffold>;
}

}












