import React from "react";
import "./Greet.css";
import { assets } from "../../assets/assets";

const Greet = () => {
    return (
        <div className="greet-page">

            <div className="hero">

                <h1>Knowledge Workspace</h1>

                <p>
                    Search, analyze and verify information across your organization's
                    documents. Every answer is grounded in retrieved sources and backed
                    by citations you can inspect.
                </p>

            </div>

           <div className="workflow-section">

    <h2>How it works</h2>

    <div className="workflow">

        <div className="workflow-step">

            <img src={assets.plus_icon} alt="" />

            <h3>Upload Documents</h3>

            <p>Add PDFs to your knowledge workspace.</p>

        </div>

        <div className="workflow-arrow">→</div>

        <div className="workflow-step">

            <img src={assets.compass_icon} alt="" />

            <h3>Semantic Retrieval</h3>

            <p>Relevant passages are retrieved for every query.</p>

        </div>

        <div className="workflow-arrow">→</div>

        <div className="workflow-step">

            <img src={assets.message_icon} alt="" />

            <h3>Grounded Answer</h3>

            <p>The model answers using only retrieved evidence.</p>

        </div>

        <div className="workflow-arrow">→</div>

        <div className="workflow-step">

            <img src={assets.code_icon} alt="" />

            <h3>Source Verification</h3>

            <p>Inspect every citation and supporting document.</p>

        </div>

    </div>

</div>

        </div>
    );
};

export default Greet;