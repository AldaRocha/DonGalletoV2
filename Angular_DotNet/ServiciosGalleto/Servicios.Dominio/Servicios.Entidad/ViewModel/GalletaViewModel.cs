using Servicios.Entidad.Model;
using System;
using System.Collections.Generic;
using System.Text;

namespace Servicios.Entidad.ViewModel
{
    public class GalletaViewModel
    {
        public int? id { get; set; }
        public string? nombre { get; set; }
        public decimal? cantidad { get; set; }
        public decimal? precioVenta { get; set; }
        public decimal? precioProduccion { get; set; }
        public string? imagen { get; set; }
        public decimal? pesoGalleta { get; set; }
        public int? idMedida { get; set; }
        public MedidaViewModel? medida { get; set; }

        public List<RecetaViewModel>? recetamodel { get; set; }
    }
}
