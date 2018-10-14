import React, { Component } from "react";
import { Container, Footer } from "./styledComponents";
import Weather from "./Weather";
import Home from "./Home";
import ErrorPage from "./Error";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

class App extends Component {
  render() {
    return (
      <Router>
        <Container>
          <Switch>
            <Route exact path="/" component={Home} />
            <Route exact path="/:city/:state/:ip" component={Weather} />
            <Route exact path="/error" component={ErrorPage} />
            <Route component={ErrorPage} />
          </Switch>
          <Footer>
            Made by: Monica Powell |{" "}
            <a href="https://github.com/M0nica/flask_weather">View on GitHub</a>
          </Footer>
        </Container>
      </Router>
    );
  }
}

export default App;
