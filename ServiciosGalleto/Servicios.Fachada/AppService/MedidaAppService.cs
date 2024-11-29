using Servicios.Datos;
using Servicios.Entidad.Model;
using Servicios.Entidad.ViewModel;
using System.Collections.Generic;
using System;
using Servicios.Fachada.DAO;

namespace Servicios.Fachada.AppService
{
    public class MedidaAppService
    {
        public List<MedidaViewModel> GetMedida(AccesoDatos DbContext)
        {
            try
            {
                MedidaDAO mdao = new MedidaDAO();

                List<Medida> lista = mdao.GetAllMedida(DbContext);
                List<MedidaViewModel> dataList = new List<MedidaViewModel>();

                foreach (Medida i in lista)
                {
                    MedidaViewModel model = new MedidaViewModel();

                    model.id = i.MedidaId;
                    model.nombre = i.Nombre;

                    dataList.Add(model);
                }

                return dataList;
            }
            catch (Exception ex)
            {
                return null;
            }
        }
    }
}
