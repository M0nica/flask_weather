import React from "react";
import { Placeholder, CardHeader, CardBody, Card } from "./styledComponents";
import { Redirect } from "react-router-dom";
import axios from "axios";
import WeatherIcon from "react-icons-weather";

class Weather extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: true,
      isError: false
    };
  }

  componentDidMount() {
    const ip = this.props.match.params.ip;
    axios
      .get(`/weather/${ip}`)
      .then(response => {
        this.setState({
          isLoading: false,
          rainCommentary: response.data.rainCommentary,
          temperature: response.data.temperature,
          hasCelsius: response.data.hasCelsius,
          icon: response.data.icon
        });
      })
      .catch(error => {
        console.log(error);
        this.setState({
          isLoading: false,
          isError: true
        });
      });
  }

  render() {
    const { city, state } = this.props.match.params;
    const {
      isLoading,
      rainCommentary,
      temperature,
      hasCelsius,
      icon,
      isError
    } = this.state;
    if (isError) {
      return <Redirect to={"/error"} />;
    }

    return (
      <Card>
        <CardHeader>Today's Weather Forecast</CardHeader>
        <CardBody>
          <div>
            {city}, {state}
          </div>
          {!isLoading ? (
            <div>
              {temperature} {hasCelsius ? "\u2103" : "\u2109"}
              <WeatherIcon
                name="darksky"
                iconId={icon}
                flip="horizontal"
                rotate="90"
              />
            </div>
          ) : (
            <Placeholder />
          )}
          {!isLoading ? (
            <div>{rainCommentary}</div>
          ) : (
            <Placeholder height="100px" />
          )}
        </CardBody>
      </Card>
    );
  }
}

export default Weather;
