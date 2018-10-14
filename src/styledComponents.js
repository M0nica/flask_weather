import styled, { keyframes } from "styled-components";

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 100%;
  align-items: center;
`;

export const Card = styled.div`
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 325px;
  transition: 0.3s;
  &:hover {
    box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
  }
`;
export const CardHeader = styled.h2`
  background-color: #7e9db4;
  padding: 0.5em;
  font-size: 30px;
  font-weight: 500;
  line-height: 1.1;
  text-align: center;
  margin: 0;
`;

export const CardBody = styled.div`
  background-color: #f8f3f3;
  padding: 2em;
  min-height: 325px;
  display: grid;
  grid-template-rows: auto auto auto;
  grid-row-gap: 16px;
  text-align: center;
  > div:first-of-type {
    font-size: 30px;
  }
  > div:nth-of-type(2) {
    font-size: 72px;
  }
`;

const placeHolderKeyframe = keyframes`
  0% {
    opacity: 0.6;
  }
  100% {
    opacity: 1;
  }
`;
export const Placeholder = styled.div`
  width: 100%;
  height: ${props => props.height || "100px"};
  background-color: #d3d3d3;
  animation: ${placeHolderKeyframe} 0.5s ease-in-out 0s infinite alternate;
`;

export const Footer = styled.footer`
  margin-top: 16px;
  > a {
    color: #007bff;
    text-decoration: none;
  }
`;

export const ErrorCard = styled.div`
  background-color: #b6ebef;
  max-width: 325px;
  padding: 20px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  text-align: center;
`;

export const Button = styled.button`
  background-color: #343a40;
  color: white;
  border: none;
  border-radius: .25rem;
  font-weight: 400;
  font-size: 1rem;
  padding: .375rem .75rem;
`;
