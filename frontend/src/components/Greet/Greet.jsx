import React from "react";
import "./Greet.css";
import { assets } from "../../assets/assets";
const Greet = () => {
    return (
        <div className="greet-page">

            <div className="hero">

                <h1>Unified Knowledge AI</h1>

                <p>
                    Turn organizational knowledge into actionable work.
                    Search across connected sources, analyze information,
                    and use AI-powered tools to move tasks forward with
                    grounded answers and verifiable results.
                </p>

            </div>

            <div className="workflow-section">

                <h2>How it works</h2>

                <div className="workflow">

                    <div className="workflow-step">

                        <img src={assets.plus_icon} alt="" />

                        <h3>Connected Knowledge</h3>

                        <p>
                            Access information across your organization's
                            connected documents and knowledge sources.
                        </p>

                    </div>

                    <div className="workflow-arrow">→</div>

                    <div className="workflow-step">

                        <img src={assets.compass_icon} alt="" />

                        <h3>Contextual Retrieval</h3>

                        <p>
                            Retrieve and combine relevant information
                            to build context for your questions and tasks.
                        </p>

                    </div>

                    <div className="workflow-arrow">→</div>

                    <div className="workflow-step">

                        <img src={assets.message_icon} alt="" />

                        <h3>Tool-assisted Work</h3>

                        <p>
                            Use AI-powered tools to analyze information
                            and carry out multi-step tasks.
                        </p>

                    </div>

                    <div className="workflow-arrow">→</div>

                    <div className="workflow-step">

                        <img src={assets.code_icon} alt="" />

                        <h3>Evidence & Verification</h3>

                        <p>
                            Inspect supporting sources and verify
                            answers and task results.
                        </p>

                    </div>

                </div>

            </div>

        </div>
    );
};

export default Greet;