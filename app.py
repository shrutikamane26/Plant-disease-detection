import 'dart:convert'; // Import for JSON encoding/decoding
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Plant Disease Detection',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  File? _image;
  String _result = '';
  String _accuracy = '';
  String _imagePath = '';

  Future<void> _pickImage() async {
    final pickedFile = await ImagePicker().getImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  Future<void> _uploadImage() async {
    if (_image == null) return;

    final request = http.MultipartRequest(
      'POST',
      Uri.parse('http://127.0.0.1:5000'), // Replace with your backend URL
    );

    request.files.add(await http.MultipartFile.fromPath(
      'file', // This should match the field name in your backend
      _image!.path,
    ));

    final response = await request.send();

    if (response.statusCode == 200) {
      final responseData = await response.stream.bytesToString();
      final responseJson = jsonDecode(responseData); // Parse the JSON response
      setState(() {
        _result = responseJson['category']; // Get the disease name
        _accuracy = responseJson['accuracy']; // Get the accuracy
        _imagePath = responseJson['image_path']; // Get the image path for display
      });
    } else {
      setState(() {
        _result = 'Error: Unable to get prediction.';
        _accuracy = '';
        _imagePath = '';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Plant Disease Detection'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            _image == null
                ? Text('No image selected.')
                : Image.file(_image!, height: 200),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImage,
              child: Text('Upload Leaf Image'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _uploadImage,
              child: Text('Predict Disease'),
            ),
            SizedBox(height: 20),
            Text(
              _result,
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 10),
            Text(
              _accuracy,
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.normal),
            ),
            SizedBox(height: 10),
            if (_imagePath.isNotEmpty) 
              Image.network('http://127.0.0.1:5000' + _imagePath), // Display uploaded image
          ],
        ),
      ),
    );
  }
}
