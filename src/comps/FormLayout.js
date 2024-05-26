import Footer from "../comps/Footer"

const { default: Navbar } = require("./Navbar");

const FormLayout = ( {children} ) => {
    return (  
        <div className="content">
            <Navbar/>
            {children}
            <Footer/>
        </div>
    );
}
 
export default FormLayout;
