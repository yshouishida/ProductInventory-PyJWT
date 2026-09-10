using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows.Forms;
using prfProductInventory.Models;

namespace prfProductInventory.Forms
{
    public partial class frmProductDE : Form
    {
        private readonly HttpClient client = ApiClient.client;
        const string BASE_URL = "http://127.0.0.1:5000/api/products";

        private int ProductId { get; set; }
        private bool IsEdit { get; set; }
        public frmProductDE()
        {
            InitializeComponent();

            IsEdit = false;
            ProductId = 0;
        }

        public frmProductDE(int ProductId, bool IsEdit)
        {
            InitializeComponent();

            this.ProductId = ProductId;
            this.IsEdit = IsEdit;
        }

        private async void ProductDE_Load(object sender, EventArgs e)
        {
            btnSave.Text = IsEdit ? "Save" : "Add";

            if (IsEdit) await GetById();
        }

        private async void btnSave_Click(object sender, EventArgs e)
        {
            if (IsEdit)
            {
                await UpdateProduct();
            }
            else
            {
                await AddProduct();
            }
        }

        private async Task UpdateProduct()
        {
            try
            {
                Product product = new Product
                {
                    id = ProductId,
                    code = txtCode.Text,
                    name = txtName.Text,
                    description = txtDesc.Text,
                    qty = Convert.ToInt32(txtQty.Text),
                    price = Convert.ToDouble(txtPrice.Text)
                };

                string json = JsonSerializer.Serialize(product);

                using (StringContent content = new StringContent(json, Encoding.UTF8, "application/json"))
                {
                    HttpResponseMessage response = await client.PutAsync($"{BASE_URL}/{ProductId}", content);

                    if (response.IsSuccessStatusCode)
                    {
                        MessageBox.Show("Updated successfully.");
                        Close();
                    }
                    else
                    {
                        MessageBox.Show(json, "Unable to update");
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Error");
            }
        }

        private async Task AddProduct()
        {
            try
            {
                Product prod = new Product
                {
                    code = txtCode.Text,
                    name = txtName.Text,
                    description = txtDesc.Text,
                    qty = Convert.ToInt32(txtQty.Text),
                    price = Convert.ToDouble(txtPrice.Text)
                };

                string json = JsonSerializer.Serialize(prod);

                using (StringContent content = new StringContent(json, Encoding.UTF8, "application/json"))
                {
                    HttpResponseMessage response = await client.PostAsync($"{BASE_URL}", content);

                    if (response.IsSuccessStatusCode)
                    {
                        MessageBox.Show("Added successfully.");
                        Close();
                    }
                    else
                    {
                        MessageBox.Show(json,"Unable to add");
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Error");
            }
        }


        private async Task GetById()
        {
            try
            {
                HttpResponseMessage response = await client.GetAsync($"{BASE_URL}/{ProductId}");
                string json = await response.Content.ReadAsStringAsync();

                if (!response.IsSuccessStatusCode)
                {
                    MessageBox.Show(json, "Unable to load");
                    return;
                }

                ApiResponse<Product> product = JsonSerializer.Deserialize<ApiResponse<Product>>(json);

                txtCode.Text = product.data.code;
                txtName.Text = product.data.name;
                txtDesc.Text = product.data.description;
                txtQty.Text = product.data.qty.ToString();
                txtPrice.Text = product.data.price.ToString("0.00");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Eror: {ex.Message}");
            }
        }

 
    }
}

