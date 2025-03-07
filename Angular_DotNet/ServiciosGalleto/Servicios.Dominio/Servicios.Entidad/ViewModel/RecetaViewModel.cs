using Servicios.Entidad.Model;
using System;
using System.Collections.Generic;
using System.Text;

namespace Servicios.Entidad.ViewModel
{
    public class RecetaViewModel
    {
        public int? id { get; set; }
        public decimal? cantidad { get; set; }
        public int? idGalleta { get; set; }
        public GalletaViewModel? galleta { get; set; }
        public int? idInventario { get; set; }
        public InventarioViewModel inventario { get; set; }
        public int idMedida { get; set; }
        public MedidaViewModel medida { get; set; }
    }
}
