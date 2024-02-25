import { ComponentProps, FC } from "react";
import { Link as RouterLink } from "react-router-dom";
import clx from "classnames";

import css from "../../style/controls.module.css";

export const Link: FC<ComponentProps<typeof RouterLink>> = ({ className, ...props }) => {
	return <RouterLink {...props} className={clx(className, css.control)} />;
};
