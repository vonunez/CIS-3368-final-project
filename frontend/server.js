// Import required modules
const express = require('express');
const app = express();
const path = require('path');
const axios = require('axios');
const bodyParser = require('body-parser'); // Import bodyParser module





// Middleware to disable caching for all routes
app.use((req, res, next) => {
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
    next();
});

app.use(bodyParser.json()); // Add this line

// Middleware to parse JSON bodies
app.use(express.json());

// Set the view engine to ejs
app.set('view engine', 'ejs');

// Define the path to the views directory
app.set('views', path.join(__dirname, 'views', 'pages'));

// Define the path to the assets directory
app.use('/assets', express.static(path.join(__dirname, 'assets')));

// Define a route for the root URL
app.get('/', (req, res) => {
    // Render the index.ejs view and pass the currentPage variable
    res.render('index', { currentPage: 'index' });
});

// Define a route for the dashboard page
app.get('/dashboard', (req, res) => {
    // Render the dashboard.ejs view and pass the currentPage variable
    res.render('dashboard', { currentPage: 'dashboard' });
});



//// Define a route to fetch facilities from the backend and render the 'facilities' view
app.get('/facilities', async (req, res) => {
    try {
      // Make a GET request to fetch facilities from the backend
      const response = await axios.get('http://127.0.0.1:5000/facilities'); // Update URL as needed
      // Extract facilities data from the response
      const facilities = response.data;
      // Render the 'facilities' view and pass the fetched facilities data along with the currentPage variable to it
      res.render('facilities', { facilities, currentPage: 'facilities' });
    } catch (error) {
      // Handle errors
      console.error('Error fetching facilities:', error.message);
      res.status(500).send('Error fetching facilities');
    }
  });
  

// Define a route to handle adding new facilities
app.post('/facilities', async (req, res) => {
  try {
    // Extract the facility name from the request body
    const facilityName = req.body.name;
    if (!facilityName) {
      throw new Error('Facility name is required');
    }
    
    // Here, you need to make a POST request to your backend API to add the facility to the database
    // For now, let's assume you're using axios to make this request
    const response = await axios.post('http://127.0.0.1:5000/facilities', { name: facilityName });
    
    // Respond with a success message
    console.log('Facility added successfully');
    res.status(200).send('Facility added successfully');
  } catch (error) {
    // Handle errors
    console.error('Error adding facility:', error.message);
    res.status(500).send(`Error adding facility: ${error.message}`);
  }
});

// Define a route to handle updating existing facilities
app.put('/facilities', async (req, res) => {
  try {
    // Extract the facility id and new name from the request body
    const facilityId = req.body.id;
    const newName = req.body.name;
    
    // Send a PUT request to update the facility in the backend
    const response = await axios.put('http://127.0.0.1:5000/facilities', { id: facilityId, name: newName });
    
    // Respond with a success message
    console.log('Facility updated successfully');
    res.status(200).send('Facility updated successfully');
  } catch (error) {
    // Handle errors
    console.error('Error updating facility:', error.message);
    res.status(500).send(`Error updating facility: ${error.message}`);
  }
});

// Define a route to handle deleting existing facilities
app.delete('/facilities', async (req, res) => {
  try {
    // Extract the facility id from the request body
    const facilityId = req.body.id;
    
    // Send a DELETE request to delete the facility in the backend
    const response = await axios.delete('http://127.0.0.1:5000/facilities', { data: { id: facilityId } });
    
    // Respond with a success message
    console.log('Facility deleted successfully');
    res.status(200).send('Facility deleted successfully');
  } catch (error) {
    // Handle errors
    console.error('Error deleting facility:', error.message);
    res.status(500).send(`Error deleting facility: ${error.message}`);
  }
});











// Define a route to fetch children from the backend along with classroom information
app.get('/children', async (req, res) => {
  try {
    // Make a GET request to fetch children from the backend
    const childrenResponse = await axios.get('http://127.0.0.1:5000/children'); // Update URL as needed
    
    // Make a GET request to fetch classroom information
    const classroomsResponse = await axios.get('http://127.0.0.1:5000/classrooms'); // Update URL as needed
    
    // Extract children and classrooms data from the responses
    const children = childrenResponse.data;
    const classrooms = classroomsResponse.data;
    
    // Render the 'children' view and pass the fetched children and classrooms data along with the currentPage variable to it
    res.render('children', { children, classrooms, currentPage: 'children' });
  } catch (error) {
    // Handle errors
    console.error('Error fetching children:', error.message);
    res.status(500).send('Error fetching children');
  }
});

  

// Define a route to handle adding new children
app.post('/children', async (req, res) => {
  try {
    // Extract child information from the request body
    const { firstname, lastname, age, room } = req.body;
    if (!firstname || !lastname || !age || !room) {
      throw new Error('All fields are required');
    }
    
    // Here, you need to make a POST request to your backend API to add the child to the database
    // For now, let's assume you're using axios to make this request
    const response = await axios.post('http://127.0.0.1:5000/children', { firstname, lastname, age, room });
    
    // Respond with a success message
    console.log('Child added successfully');
    res.status(200).send('Child added successfully');
  } catch (error) {
    // Handle errors
    console.error('Error adding child:', error.message);
    res.status(500).send(`Error adding child: ${error.message}`);
  }
});

// Define a route to handle updating existing children
app.put('/children', async (req, res) => {
  try {
    // Extract the child id and new information from the request body
    const { id, firstname, lastname, age, room } = req.body;
    
    // Send a PUT request to update the child in the backend
    const response = await axios.put('http://127.0.0.1:5000/children', { id, firstname, lastname, age, room });
    
    // Respond with a success message
    console.log('Child updated successfully');
    res.status(200).send('Child updated successfully');
  } catch (error) {
    // Handle errors
    console.error('Error updating child:', error.message);
    res.status(500).send(`Error updating child: ${error.message}`);
  }
});

// Define a route to handle deleting existing children
app.delete('/children', async (req, res) => {
  try {
    // Extract the child id from the request body
    const { id } = req.body;
    
    // Send a DELETE request to delete the child in the backend
    const response = await axios.delete('http://127.0.0.1:5000/children', { data: { id } });
    
    // Respond with a success message
    console.log('Child deleted successfully');
    res.status(200).send('Child deleted successfully');
  } catch (error) {
    // Handle errors
    console.error('Error deleting child:', error.message);
    res.status(500).send(`Error deleting child: ${error.message}`);
  }
});





// Define a route to fetch classrooms from the backend and render the 'classrooms' view
app.get('/classrooms', async (req, res) => {
  try {
    // Make a GET request to fetch classrooms from the backend
    const classroomsResponse = await axios.get('http://127.0.0.1:5000/classrooms'); // Update URL as needed
    // Make a GET request to fetch facilities from the backend
    const facilitiesResponse = await axios.get('http://127.0.0.1:5000/facilities'); // Update URL as needed
    
    // Extract classrooms data from the response
    const classrooms = classroomsResponse.data;
    // Extract facilities data from the response
    const facilities = facilitiesResponse.data;
    
    // Render the 'classrooms' view and pass the fetched classrooms and facilities data along with the currentPage variable to it
    res.render('classrooms', { classrooms, facilities, currentPage: 'classrooms' });
  } catch (error) {
    // Handle errors
    console.error('Error fetching classrooms:', error.message);
    res.status(500).send('Error fetching classrooms');
  }
});


// Define a route to handle adding new classrooms
app.post('/classrooms', async (req, res) => {
try {
  // Extract classroom information from the request body
  const { name, capacity, facility_id } = req.body;
  if (!name || !capacity || !facility_id) {
    throw new Error('All fields are required');
  }
  
  // Here, you need to make a POST request to your backend API to add the classroom to the database
  // For now, let's assume you're using axios to make this request
  const response = await axios.post('http://127.0.0.1:5000/classrooms', { name, capacity, facility_id });
  
  // Respond with a success message
  console.log('Classroom added successfully');
  res.status(200).send('Classroom added successfully');
} catch (error) {
  // Handle errors
  console.error('Error adding classroom:', error.message);
  res.status(500).send(`Error adding classroom: ${error.message}`);
}
});

// Define a route to handle updating existing classrooms
app.put('/classrooms', async (req, res) => {
try {
  // Extract the classroom id and new information from the request body
  const { id, name, capacity, facility_id } = req.body;
  
  // Send a PUT request to update the classroom in the backend
  const response = await axios.put('http://127.0.0.1:5000/classrooms', { id, name, capacity, facility_id });
  
  // Respond with a success message
  console.log('Classroom updated successfully');
  res.status(200).send('Classroom updated successfully');
} catch (error) {
  // Handle errors
  console.error('Error updating classroom:', error.message);
  res.status(500).send(`Error updating classroom: ${error.message}`);
}
});

// Define a route to handle deleting existing classrooms
app.delete('/classrooms', async (req, res) => {
try {
  // Extract the classroom id from the request body
  const { id } = req.body;
  
  // Send a DELETE request to delete the classroom in the backend
  const response = await axios.delete('http://127.0.0.1:5000/classrooms', { data: { id } });
  
  // Respond with a success message
  console.log('Classroom deleted successfully');
  res.status(200).send('Classroom deleted successfully');
} catch (error) {
  // Handle errors
  console.error('Error deleting classroom:', error.message);
  res.status(500).send(`Error deleting classroom: ${error.message}`);
}
});







// Define a route to fetch teachers from the backend and render the 'teachers' view
app.get('/teachers', async (req, res) => {
  try {
    // Make a GET request to fetch teachers from the backend
    const teachersResponse = await axios.get('http://127.0.0.1:5000/teachers'); // Update URL as needed
    // Make a GET request to fetch classrooms from the backend
    const classroomsResponse = await axios.get('http://127.0.0.1:5000/classrooms'); // Update URL as needed
    
    // Extract teachers data from the response
    const teachers = teachersResponse.data;
    // Extract classrooms data from the response
    const classrooms = classroomsResponse.data;
    
    // Render the 'teachers' view and pass the fetched teachers and classrooms data along with the currentPage variable to it
    res.render('teachers', { teachers, classrooms, currentPage: 'teachers' });
  } catch (error) {
    // Handle errors
    console.error('Error fetching teachers:', error.message);
    res.status(500).send('Error fetching teachers');
  }
});




// Define a route to fetch teachers from the backend along with classroom information
app.get('/teachers', async (req, res) => {
  try {
    // Make a GET request to fetch teachers from the backend
    const teachersResponse = await axios.get('http://127.0.0.1:5000/teachers'); // Update URL as needed
    
    // Make a GET request to fetch classroom information
    const classroomsResponse = await axios.get('http://127.0.0.1:5000/classrooms'); // Update URL as needed
    
    // Extract teachers and classrooms data from the responses
    const teachers = teachersResponse.data;
    const classrooms = classroomsResponse.data;
    
    // Render the 'teachers' view and pass the fetched teachers and classrooms data along with the currentPage variable to it
    res.render('teachers', { teachers, classrooms, currentPage: 'teachers' });
  } catch (error) {
    // Handle errors
    console.error('Error fetching teachers:', error.message);
    res.status(500).send('Error fetching teachers');
  }
});

// POST route to handle adding a new teacher
app.post('/teachers', async (req, res) => {
  try {
    // Extract teacher information from the request body
    const { firstname, lastname, room } = req.body;
    
    // Validate the presence of all required fields
    if (!firstname || !lastname || !room) {
      throw new Error('All fields are required');
    }
    
    // Make a POST request to your backend API to add the teacher to the database
    const response = await axios.post('http://127.0.0.1:5000/teachers', { firstname, lastname, room });
    
    // Respond with the response from the backend server
    res.status(response.status).json(response.data);
  } catch (error) {
    // Handle errors
    console.error('Error adding teacher:', error.message);
    res.status(500).json({ error: `Error adding teacher: ${error.message}` });
  }
});




app.put('/teachers', async (req, res) => {
  try {
      // Extract the teacher id and new information from the request body
      const { id, firstname, lastname, room } = req.body;
      
      // Send a PUT request to update the teacher in the backend
      const response = await axios.put('http://127.0.0.1:5000/teachers', { id, firstname, lastname, room });
      
      // Respond with a success message
      console.log('Teacher updated successfully');
      res.status(200).send('Teacher updated successfully');
  } catch (error) {
      // Handle errors
      console.error('Error updating teacher:', error.message);
      res.status(500).send(`Error updating teacher: ${error.message}`);
  }
});

app.delete('/teachers', async (req, res) => {
  try {
      // Extract the teacher id from the request body
      const { id } = req.body;
      
      // Send a DELETE request to delete the teacher in the backend
      const response = await axios.delete('http://127.0.0.1:5000/teachers', { data: { id } });
      
      // Respond with a success message
      console.log('Teacher deleted successfully');
      res.status(200).send('Teacher deleted successfully');
  } catch (error) {
      // Handle errors
      console.error('Error deleting teacher:', error.message);
      res.status(500).send(`Error deleting teacher: ${error.message}`);
  }
});







// Define a route for handling login requests
app.post('/login', (req, res) => {
    // Implement the logic to authenticate the user
    const { username, password } = req.body;

    // Example authentication logic (replace with your actual logic)
    if (username === 'admin' && password === 'new_password') {
        // Authentication successful
        res.send({ message: 'Login successful' });
    } else {
        // Authentication failed
        res.status(401).send({ error: 'Invalid credentials' });
    }
});


// Define a route for logging out
app.get('/logout', (req, res) => {
    // Implement the logout logic here
    // For example, you can clear the session or remove the user's authentication token
    
    // Redirect the user to the login page after logout
    res.redirect('/');
});


// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
