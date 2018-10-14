import React from "react";
import axios from "axios";
import { Redirect } from "react-router-dom"
class Home extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: true,
      isError: false
    };
  }

  componentDidMount() {
    axios.get(`/getLocationByIP`).then(response => {
        this.setState({
            city: response.data.city,
            state: response.data.state,
            ip: response.data.ip_coords,
            isLoading: false
        })
    }).catch(error => {
        console.log(error);
        this.setState({
            isLoading: false,
            isError: true
        })
    });
  }

  render() {
    const { isLoading, city, state, ip, isError } = this.state;
    if(isError) {
        return  <Redirect to={"/error"} />
    }

    if(isLoading){
        return <div> Loading..</div>
    }
  
    return <Redirect to={`/${city}/${state}/${ip}`} />
    
  }
}

export default Home;
