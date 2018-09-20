/*
    Note : To compile this example, using g++, use :

    g++ -o use_libgmic use_libgmic.cpp -lgmic -lfftw3
*/

/*
  Uncomment the two lines below if you want to use the CImg library along with the G'MIC library.
 */
//#include "CImg.h"
//using namespace cimg_library;

#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <pybind11/cast.h>
#include "gmic.h"
#include <cstdio>
#include <cmath>
#include<vector>
#include<string>
#include<list>
#include <iostream>

#include <pybind11/pybind11.h>
namespace py = pybind11;

using namespace std;





typedef py::array_t<float, py::array::c_style | py::array::forcecast> np_img;






template<typename val> void print_vec(const std::vector<val>& vec)
{

    std::cout << "<";
    for (auto x: vec)
    {
        std::cout << ' ' << x;
    }
    std::cout << ">\n";
};

/*class python_gmic_image: public py::object
{
   public:
   gmic_image<float> img;
  // python_gmic_image(const gmic_image<float>& m):img(m){};
};
*/

//gmic_image<T>
 py::buffer_info get_image_buffer(gmic_image<float>& m)
{


    auto buf= py::buffer_info( m._data,                               // Pointer to buffer
                          sizeof(m(0)),                          // Size of one scalar
                          py::format_descriptor< float>::format(), // Python struct-style format descriptor
                          4,                                      // Number of dimensions
    { m._width, m._height,m._depth,m._spectrum },                 // Buffer dimensions
    {
        sizeof(m(0)),sizeof(m(0)) *m._width, sizeof(m(0)) *m._width*m._height,
        sizeof(m(0)) *m._width*m._height*m._depth
        //Strides (in bytes) for each index
    });

    return buf;

};




//template<typename T>
 py::object get_img_array( gmic_list<float> &images)
{
    //py::object res_img = py::list();
    py::list res_img;


    for(ssize_t n =0; n<images._width; n++)
    {
        //auto img=images[n];
        auto res_i = get_image_buffer( images[n]) ;
        //auto res_i =  py::buffer_info();
        if (res_i.size!=0)
        {
         py::array  res_array(res_i);
         //res_img.attr("append")(  res_array);
         res_img.append(res_array);
        }

    };

    return res_img;
}






gmic_list<float> images;
gmic_list<char> images_names;

void reset()
{
    images.assign(0U);
    images_names.assign(0U);

}



//vector<gmic_image<float>>
py::list gmic_call(std::string cmd,std::vector<np_img> &imgs,std::vector<std::string> &names)
{
    gmic gmic_instance;
    reset();
    ssize_t nb_img=imgs.size();
    ssize_t nb_names=names.size();


    images.assign(nb_img);

    images_names.assign(nb_names);





    for (ssize_t n =0; n<nb_img; n++)
    {
        np_img im=imgs[n];
        std::vector<ssize_t> shape;
        std::cout<<im.ndim()<<endl;
        //shape.assign((ssize_t) im.ndim(),*im.shape());
        {



            auto imshape=im.shape();
            for (ssize_t i =0; i<im.ndim(); i++)
                shape.push_back(imshape[i]);
        }





        print_vec(shape);


        /*if (im.ndim()==3)
        {
            int depth=1;
            shape.insert(shape.begin()+3,depth);
            im.resize(shape);
        }*/


        auto r=im.unchecked<float,4>(); ;
        images[n].assign(shape[0],shape[1],shape[2],shape[3]);

        for (ssize_t i = 0; i < shape[0]; i++)
            for (ssize_t j = 0; j < shape[1]; j++)
                for (ssize_t k = 0; k < shape[2]; k++)
                    for (ssize_t c = 0; c < shape[3]; c++)
                        images[n](i,j,k,c)= r(i, j, k,c);

    }
    auto cmd_char=cmd.c_str();
    {

        py::gil_scoped_release rel;

        gmic_instance.run(cmd_char,images,images_names);



    }


        return  get_img_array(images);





}









PYBIND11_MODULE(gmicpy, m)
{
    m.doc() = "libgmic bindings"; // optional module docstring


    m.def("gmic_call", &gmic_call,  py::return_value_policy::copy);
    m.def("reset", &reset);

    /*py::class_<gmic_image<float>>(m, "gmic_image", py::buffer_protocol())

                               .def_buffer([](gmic_image<float> &m) -> py::buffer_info
    {
        return get_image_buffer(m);
    });*/

    //py::class_<gmic_list<float>>(m, "gmic_list")



}






