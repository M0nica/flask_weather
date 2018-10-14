import React from "react";
import { ErrorCard, Button } from "./styledComponents";

const ErrorPage = () => (
    <ErrorCard>
         Whoops! Something went wrong. <br /> Feel free to create an issue! ❤️
        <br />
        <a href="/">
            <Button type="button">Retry</Button>
        </a>
    </ErrorCard>
)

export default ErrorPage;