import React from 'react';

const Skeleton = ({ className, height, width, variant = 'rect' }) => {
    const baseStyles = "animate-pulse bg-slate-200 rounded";
    const variants = {
        circle: "rounded-full",
        rect: "rounded-md",
        text: "rounded-sm h-4 w-3/4"
    };

    const style = {
        height: height,
        width: width,
    };

    return (
        <div
            className={`${baseStyles} ${variants[variant]} ${className || ''}`}
            style={style}
        />
    );
};

export default Skeleton;
