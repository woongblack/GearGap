export default function Background() {
  return (
    <>
      <div className="bg-layer bg-vignette"></div>
      <div className="bg-layer bg-grid"></div>
      <div className="bg-layer bg-sigil">
        <svg width="900" height="900" viewBox="0 0 900 900" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <circle cx="450" cy="450" r="380" stroke="#c2a25b" strokeWidth="1"/>
          <circle cx="450" cy="450" r="300" stroke="#c2a25b" strokeWidth="1" strokeDasharray="2 8"/>
          <circle cx="450" cy="450" r="220" stroke="#c2a25b" strokeWidth="1"/>
          <polygon points="450,180 690,580 210,580" stroke="#c2a25b" strokeWidth="1" fill="none"/>
          <polygon points="450,720 210,320 690,320" stroke="#c2a25b" strokeWidth="1" fill="none"/>
          <circle cx="450" cy="450" r="60" stroke="#c2a25b" strokeWidth="1"/>
        </svg>
      </div>
      <div className="bg-layer bg-grain"></div>
    </>
  );
}
