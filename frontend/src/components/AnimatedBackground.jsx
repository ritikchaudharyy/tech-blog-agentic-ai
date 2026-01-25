const AnimatedBackground = () => {
  return (
    <div className="absolute inset-0 -z-10 overflow-hidden">
      <div className="absolute -top-32 -left-32 w-[28rem] h-[28rem] bg-blue-500/30 dark:bg-blue-600/20 rounded-full blur-3xl animate-blob" />
      <div className="absolute top-1/3 -right-32 w-[30rem] h-[30rem] bg-indigo-500/30 dark:bg-indigo-600/20 rounded-full blur-3xl animate-blob animation-delay-2000" />
      <div className="absolute bottom-[-8rem] left-1/4 w-[26rem] h-[26rem] bg-sky-400/30 dark:bg-sky-500/20 rounded-full blur-3xl animate-blob animation-delay-4000" />
    </div>
  );
};

export default AnimatedBackground;
