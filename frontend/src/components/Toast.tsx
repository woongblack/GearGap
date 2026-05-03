interface ToastProps {
  msg: string;
  show: boolean;
}

export default function Toast({ msg, show }: ToastProps) {
  return (
    <div className={`toast ${show ? 'show' : ''}`} role="status" aria-live="polite">
      <span className="spin"></span><span>{msg}</span>
    </div>
  );
}
