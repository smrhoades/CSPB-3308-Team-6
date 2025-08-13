import './footer.css'

export default function Footer() {
    const teamMembers = [
        "Daniel Williams",
        "Sara Rhoades",
        "Joey Musholt",
        "Joel Henry"
    ];

    return (
        <footer className="footer">
            <div className="footer-image">
            <img src="../favicon.ico" alt="team logo"
                 width="100" height="100"
            />
            </div>
            <div className="footer-text-content">
                <p><strong>Team 6 Developers</strong></p>
                <p>{teamMembers.join(", ")}</p>
                <p>CSPB3308 Class Project, Summer 2025</p>
                {/* <p>Summer 2025</p> */}
            </div>
        </footer>
    );
}