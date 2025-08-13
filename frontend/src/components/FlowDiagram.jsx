import React from "react";
// import { awsIcon } from "../utils/awsIcons";

import AWSLambda from "../assets/aws/compute/AWS-Lambda.svg";
import AmazonS3 from "../assets/aws/storage/Amazon-S3.svg";
import AmazonRDS from "../assets/aws/database/Amazon-RDS.svg";

const iconMap = {
  "AWS-Lambda": AWSLambda,
  "Amazon-S3": AmazonS3,
  "Amazon-RDS": AmazonRDS,
};

const awsIcon = (name) => iconMap[name] || iconMap["AWS-Lambda"];

function FlowDiagram() {
  return (
    <div className="flow-diagram flex items-center justify-center p-6 bg-transparent">
      {/* Example AWS flow */}
      <div className="flex items-center space-x-6">
        {/* Source */}
        <div className="flex flex-col items-center">
          <img
            src={awsIcon("AWS-Lambda")}
            alt="Lambda"
            width={60}
            height={60}
          />
          <span className="mt-2 text-sm">Lambda</span>
        </div>

        {/* Arrow */}
        <span className="text-2xl">➡</span>

        {/* Middle */}
        <div className="flex flex-col items-center">
          <img
            src={awsIcon("Amazon-S3")}
            alt="S3"
            width={60}
            height={60}
          />
          <span className="mt-2 text-sm">Amazon S3</span>
        </div>

        {/* Arrow */}
        <span className="text-2xl">➡</span>

        {/* Destination */}
        <div className="flex flex-col items-center">
          <img
            src={awsIcon("Amazon-RDS")}
            alt="RDS"
            width={60}
            height={60}
          />
          <span className="mt-2 text-sm">Amazon RDS</span>
        </div>
      </div>
    </div>
  );
}

export default FlowDiagram;
