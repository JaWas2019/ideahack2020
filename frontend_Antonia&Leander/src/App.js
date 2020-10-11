import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import { Button, AppBar } from '@material-ui/core'
import Nav from './components/layout/Nav';
import Hero from './components/layout/Hero';
import Footer from './components/layout/Footer'
import Feature from './components/layout/Feature';
import SignInRecruiter from './components/SignInRecruiter';
import SignIn from './components/SignIn'
import { Route, Switch } from "react-router-dom";
import BrowseJobsEmployee from './components/BrowseJobsEmployee'
//import './app.css'


class App extends Component {
  /* state = */
  render() {
    return (
        <div className="App">
          <Nav />
          <Hero />
          
          <Switch>
            <Route path="/" exact>
              <div>
                <Feature 
                  title='Faster Hiring' 
                  message1='It takes in average 43 days to fill a vacant positions. Every day conveys lost productivity that never can be recouped.'
                  message2='Fill an open position within days by promoting existing employees who have the skills to step up and are already familiar with your culture.'
                />
                <Feature 
                  title='Better Fit' 
                  message1='Resumes serve merely as a proxy for performance. And we all have at least one story of somebody who was brilliant during interviews but failed on the job.' 
                  message2='Andromeda uses AI to analyze job descriptions and match them with your employees’ skill profiles.'
                />
                <Feature 
                  title='Low-cost Recruiting' 
                  message1='Recruiting is expensive. There are job boards, head hunters, CV screening, numerous first interviews, and so on.' 
                  message2='Stay within your budget by recruiting internal employees.'
                />
              </div>
            </Route>
            <Route path='/sign-in-employee'><SignIn /></Route>
            <Route path='/browse-jobs-employee'><BrowseJobsEmployee /></Route>
        </Switch>
          <Footer />
        </div>
    );
  }
}
export default App;


/*
function App(){
  return(
  <Router>
    <div className = "App">
      <Nav />
      <h1>Welcome To Andromeda</h1>
      <a>{SignIn()}</a>
      <Route path= "/sign_in_employee" components={sign_in_employee} />
  </div>
  </Router>

  );

}


ReactDOM.render(App, document.getElementById('root'));


export default App;


ReactDOM.render(

  <Router>
   <div className = "App">
      <Nav />
      <h1>Welcome To Andromeda</h1>
      <a>{SignIn()}</a>
      <Route path= "/sign_in_employee" components={sign_in_employee} />
  </div>
  </Router>
  document.getElementById('root')
);
*/