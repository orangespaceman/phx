/**
 * PaypalKit
 *

This module exports an instance of the `PaypalKit` class.
To initialise it:

```
import paypalKit from "path/to/PaypalKit.js";
paypalKit.init();
```


It expects the following HTML content to be present:

```
<div class="PaypalKit"></div>
<script
  src="https://www.paypal.com/sdk/js?client-id=xxxxx&enable-funding=venmo&currency=GBP"
  data-sdk-integration-source="button-factory"
></script>
```


It expects the following JS content to be present:

```
<script>
  var chestSizeAll = [
    '26" / 66cm',
    '27" / 69cm',
  ];
  var chestSizeCycleJerseys = [
    '38" / 97cm',
    '39" / 99cm',
  ];
  var heights = [
    "4' / 122cm",
    "4'1\" / 124cm",
  ];

  var categories = [
    {
      category: "Running",
      items: [
        {
          description: "Running white vest (female)",
          price: 12,
          options: chestSizeAll,
        },
        {
          description: "Running white vest (male)",
          price: 12,
          options: chestSizeAll,
        },
      ],
    },
    {
      category: "Cycling",
      items: [
        {
          description: "Cycling white jersey short sleeve",
          price: 36,
          options: chestSizeCycleJerseys,
        },
      ]
    },
  ];
</script>
```
 *
 */
class PaypalKit {
  constructor() {
    // HTML elements
    this.els = {
      container: null,
      name: null,
      chestSize: null,
      height: null,
      items: null,
      order: null,
      orderItems: null,
      orderTotal: null,
      submit: null,
    };

    // CONST values used by Paypal
    this.ORDER_TITLE = "PHX-Kit";
    this.ORDER_SHIPPING = 0;
    this.ORDER_TAX = 0;

    // order values
    this.orderTotalValue = 0;
    this.orderItems = [];
    this.selectedChestSize = null;
    this.selectedHeight = null;

    // import global (window) variables
    this.paypal = window.paypal;
    this.categories = window.categories || [];
    this.chestSizeAll = window.chestSizeAll || [];
    this.heights = window.heights || [];
  }

  init() {
    this.els.container = document.querySelector(".PaypalKit");
    if (!this.els.container) return false;

    this.addInitialHTML();
    this.selectElements();
    this.addListeners();
    this.addSelectContent();
    this.initPaypal();
    this.updateOrder();
  }

  /**
   * Quick hacky way to insert the initial HTML template
   */
  addInitialHTML() {
    const template = `
      <div class="PaypalKit-orderDetails">
        <div class="Editorial">
          <h3>Your order</h3>
        </div>
        <div class="Form">
          <div class="Form-row">
            <label class="Form-label" for="contact-details">Full name:</label>
            <input
              type="text"
              name="contact-details"
              class="Form-input--text Form-input--inline PaypalKit-input--name"
            />
          </div>
          <div class="Form-row">
            <label class="Form-label" for="chest-size">Chest size:</label>
            <div class="Form-selectWrap Form-selectWrap--inline">
              <select
                name="chest-size"
                class="Form-select PaypalKit-select--chestSize"
              >
                <option value="">Please select</option>
              </select>
            </div>
          </div>
          <div class="Form-row">
            <label class="Form-label" for="height">Height:</label>
            <div class="Form-selectWrap Form-selectWrap--inline">
              <select name="height" class="Form-select PaypalKit-select--height">
                <option value="">Please select</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      <div class="PaypalKit-items Form"></div>
      <div class="PaypalKit-order u-hidden">
        <div class="Editorial">
          <h3>Order summary</h3>
        </div>
        <div class="Table">
          <table>
            <tbody class="PaypalKit-orderItems"></tbody>
            <tfoot>
              <tr>
                <th colspan="3">Total</th>
                <th class="PaypalKit-orderTotal"></th>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
      <div class="PaypalKit-submit u-hidden"></div>
    `;
    this.els.container.innerHTML = template;
  }

  /**
   * Select all elements used throughout script
   */
  selectElements() {
    // temporary short variable name referencing the root container element
    const c = this.els.container;

    // select elements
    this.els.name = c.querySelector(".PaypalKit-input--name");
    this.els.chestSize = c.querySelector(".PaypalKit-select--chestSize");
    this.els.height = c.querySelector(".PaypalKit-select--height");
    this.els.items = c.querySelector(".PaypalKit-items");
    this.els.order = c.querySelector(".PaypalKit-order");
    this.els.orderItems = c.querySelector(".PaypalKit-orderItems");
    this.els.orderTotal = c.querySelector(".PaypalKit-orderTotal");
    this.els.submit = c.querySelector(".PaypalKit-submit");
  }

  /**
   * Add triggers to fire on input change
   */
  addListeners() {
    this.els.name.addEventListener("input", this.updateOrder.bind(this));
    this.els.chestSize.addEventListener("change", this.updateOrder.bind(this));
    this.els.height.addEventListener("change", this.updateOrder.bind(this));
  }

  /**
   * Add dynamic kit content to select elements
   */
  addSelectContent() {
    // add chest size options to select
    this.chestSizeAll.forEach((size) => {
      const option = document.createElement("option");
      option.value = size;
      option.textContent = size;
      this.els.chestSize.appendChild(option);
    });

    // add height options to select
    this.heights.forEach((size) => {
      const option = document.createElement("option");
      option.value = size;
      option.textContent = size;
      this.els.height.appendChild(option);
    });

    // add categories/items
    this.categories.forEach((category, categoryIndex) => {
      const categoryTitleEl = document.createElement("h3");
      categoryTitleEl.classList.add("PaypalKit-categoryTitle");
      categoryTitleEl.textContent = category.category;
      this.els.items.appendChild(categoryTitleEl);

      category.items.forEach((item, itemIndex) => {
        const itemDivEl = document.createElement("div");
        itemDivEl.classList.add(
          "PaypalKit-item",
          `PaypalKit-item-${categoryIndex}-${itemIndex}`
        );
        this.els.items.appendChild(itemDivEl);

        const itemSelectWrapEl = document.createElement("div");
        itemSelectWrapEl.classList.add(
          "PaypalKit-itemSelectWrap",
          "Form-selectWrap",
          "Form-selectWrap--inline"
        );
        itemDivEl.appendChild(itemSelectWrapEl);

        const itemSelectEl = document.createElement("select");
        itemSelectEl.classList.add("PaypalKit-itemSelect", "Form-select");
        itemSelectEl.addEventListener("change", this.updateOrder.bind(this));
        itemSelectWrapEl.appendChild(itemSelectEl);

        for (let counter = 0; counter <= 5; counter++) {
          const optionEl = document.createElement("option");
          optionEl.textContent = counter;
          itemSelectEl.appendChild(optionEl);
        }

        const labelEl = document.createElement("label");
        labelEl.textContent = `${item.description} (£${item.price})`;
        itemDivEl.appendChild(labelEl);
      });
    });
  }

  /**
   * Init Paypal Button
   */
  initPaypal() {
    if (!this.paypal) {
      console.log("No paypal available");
      return;
    }
    this.paypal
      .Buttons({
        style: {
          shape: "rect",
          color: "black",
          layout: "vertical",
          label: "buynow",
        },
        createOrder: (data, actions) => {
          const description = `${this.ORDER_TITLE}: ${this.els.name.value}`;
          const cart = [...this.orderItems];

          cart.push({
            name: description,
            unit_amount: {
              currency_code: "GBP",
              value: 0,
            },
            quantity: 1,
          });

          return actions.order.create({
            purchase_units: [
              {
                description: description,
                amount: {
                  currency_code: "GBP",
                  value: this.orderTotalValue,
                  breakdown: {
                    item_total: {
                      currency_code: "GBP",
                      value: this.orderTotalValue,
                    },
                    shipping: {
                      currency_code: "GBP",
                      value: this.ORDER_SHIPPING,
                    },
                    tax_total: {
                      currency_code: "GBP",
                      value: this.ORDER_TAX,
                    },
                  },
                },
                items: cart,
              },
            ],
          });
        },
        onApprove: (data, actions) => {
          return actions.order.capture().then(() => {
            // Show a success message within this page
            this.els.submit.textContent = "Thank you for your payment!";
          });
        },
        onError: function (err) {
          console.log(err);
        },
      })
      .render(".PaypalKit-submit");
  }

  /**
   * Recheck the order every time something is updated
   */
  updateOrder() {
    this.updateOrderContent();
    this.updateOrderValidity();
  }

  /**
   * Update order summary
   */
  updateOrderContent() {
    // reset order values
    this.orderTotalValue = 0;
    this.orderItems = [];

    // remove existing order summary
    while (this.els.orderItems.firstChild) {
      this.els.orderItems.removeChild(this.els.orderItems.lastChild);
    }

    this.addOrderTableHeadRow();

    // retrieve selected values
    this.selectedChestSize =
      this.els.chestSize.options[this.els.chestSize.selectedIndex].value;
    this.selectedHeight =
      this.els.height.options[this.els.height.selectedIndex].value;

    // check all selected items for validity
    // if chest size or height has been updated, the product may not be valid
    this.categories.forEach((category, categoryIndex) => {
      category.items.forEach((item, itemIndex) => {
        const itemEl = document.querySelector(
          `.PaypalKit-item-${categoryIndex}-${itemIndex}`
        );
        const selectEl = itemEl.querySelector(".PaypalKit-itemSelect");

        // check if the item is available in the selected size
        if (
          item.options.includes(this.selectedChestSize) ||
          item.options.includes(this.selectedHeight)
        ) {
          selectEl.disabled = false;
          itemEl.classList.remove("PaypalKit-item--unavailable");
          const count = parseInt(
            selectEl.options[selectEl.selectedIndex].index,
            10
          );
          if (count > 0) {
            this.addCartItem(item, count);
          }
        } else {
          itemEl.classList.add("PaypalKit-item--unavailable");
          selectEl.selectedIndex = 0;
          selectEl.disabled = true;
        }
      });
    });
  }

  /**
   * Check if the order is valid before displaying paypal button
   */
  updateOrderValidity() {
    // if there are orders, show order summary
    if (this.orderTotalValue > 0 && this.orderItems.length > 0) {
      this.els.orderTotal.textContent = `£${this.orderTotalValue}`;
      this.els.order.classList.remove("u-hidden");
    } else {
      this.els.order.classList.add("u-hidden");
    }

    // if the user has entered all required info, show paypal
    if (
      this.els.name.value.length >= 2 &&
      this.selectedChestSize &&
      this.selectedHeight &&
      this.orderTotalValue > 0 &&
      this.orderItems.length > 0
    ) {
      this.els.submit.classList.remove("u-hidden");
    } else {
      this.els.submit.classList.add("u-hidden");
    }
  }

  addOrderTableHeadRow() {
    const tableHeadRowEl = document.createElement("tr");
    this.els.orderItems.appendChild(tableHeadRowEl);

    const item = document.createElement("td");
    item.textContent = "Item";
    tableHeadRowEl.appendChild(item);

    const itemPriceEl = document.createElement("td");
    itemPriceEl.textContent = "Item Price";
    tableHeadRowEl.appendChild(itemPriceEl);

    const quantityEl = document.createElement("td");
    quantityEl.textContent = "Quantity";
    tableHeadRowEl.appendChild(quantityEl);

    const totalEl = document.createElement("td");
    totalEl.textContent = "Total";
    tableHeadRowEl.appendChild(totalEl);
  }

  /**
   * Add the item to the PayPal cart, and calculate total order value
   */
  addCartItem(item, count) {
    let itemTotal = count * item.price;
    this.orderTotalValue += itemTotal;

    this.orderItems.push({
      name: `${item.description} (${this.selectedChestSize}; ${this.selectedHeight})`,
      unit_amount: {
        currency_code: "GBP",
        value: item.price,
      },
      quantity: count,
    });

    const orderRowEl = document.createElement("tr");
    this.els.orderItems.appendChild(orderRowEl);

    const descriptionEl = document.createElement("td");
    orderRowEl.appendChild(descriptionEl);

    const itemDescriptionEl = document.createElement("span");
    itemDescriptionEl.textContent = item.description;
    itemDescriptionEl.classList.add("PaypalKit-orderItemDescription");
    descriptionEl.appendChild(itemDescriptionEl);

    const itemChestSizeEl = document.createElement("span");
    itemChestSizeEl.textContent = `Chest size: ${this.selectedChestSize}`;
    itemChestSizeEl.classList.add("PaypalKit-orderItemSize");
    descriptionEl.appendChild(itemChestSizeEl);

    const itemHeightEl = document.createElement("span");
    itemHeightEl.textContent = `Height: ${this.selectedHeight}`;
    itemHeightEl.classList.add("PaypalKit-orderItemSize");
    descriptionEl.appendChild(itemHeightEl);

    const priceEl = document.createElement("td");
    priceEl.textContent = `£${item.price}`;
    orderRowEl.appendChild(priceEl);

    const countEl = document.createElement("td");
    countEl.textContent = count;
    orderRowEl.appendChild(countEl);

    const totalEl = document.createElement("td");
    totalEl.textContent = `£${itemTotal}`;
    orderRowEl.appendChild(totalEl);
  }
}

const paypalKit = new PaypalKit();

export default paypalKit;
