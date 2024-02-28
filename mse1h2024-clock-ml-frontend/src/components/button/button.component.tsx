import React, { FC } from "react";
import clx from "classnames";
import css from "../../style/controls.module.css";

export const Button: FC<React.ButtonHTMLAttributes<HTMLButtonElement>> = ({
	className,
	...props
}) => {
	return <button {...props} className={clx(className, css.control)} />;
};
