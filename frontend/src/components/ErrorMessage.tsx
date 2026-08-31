type ErrorMessageProps = { message: string };
function ErrorMessage({ message }: ErrorMessageProps) {
  if (!message) {
    return null;
  }
  return (
    <div className="mt-5 bg-red-950/50 border border-red-800 text-red-300 rounded-xl px-5 py-3">
      {" "}
      {message}{" "}
    </div>
  );
}
export default ErrorMessage;
