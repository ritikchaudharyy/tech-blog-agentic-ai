const Loader = ({ text = 'Loading…' }) => {
  return (
    <p className="text-sm text-muted">
      {text}
    </p>
  );
};

export default Loader;
