'use strict';

const APICommunicationError = (name, message) => {
    this.message = message;
    this.name = name;
}


/**
 * Communicate with API
 * @param {string} endpoint
 * @param {string} requestType
 * @param {object} dataPackage
 * @param {boolean} isLocalhost
 */
const communication = async (endpoint, requestType = "GET", dataPackage = null, isLocalhost = false) => {
    let API = "http://logos.sch.ac.kr:40101/api/";

    let requestOptions = {
        method: requestType,
        cache: "no-cache",
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (dataPackage !== null) requestOptions["body"] = JSON.stringify(dataPackage);
    const communication = await fetch(`${(isLocalhost) ? "" : API}${endpoint}`, requestOptions)
        .catch(error => {
            error = error.toString().split(": ");
            // throw new APICommunicationError("Can't receive data", "Database may not created or API Service is down for now.");
            return "error";
            // throw new APICommunicationError(error[0], error[1]);
        });
    const dataset = await communication.json();
    if (communication.ok) return dataset;
    if (!communication.ok) {
        // throw new APICommunicationError("Error", communication.statusText);
        return "error";
    }
}


module.exports = {communication};
