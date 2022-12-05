/**
 * PaypalTickets
 *

This module exports an instance of the `PaypalTickets` class.
To initialise it:

```
import paypalTickets from "path/to/PaypalTickets.js";
paypalTickets.init();
```


It expects the following HTML content to be present:

```
<div class="PaypalTickets"></div>
<script
  src="https://www.paypal.com/sdk/js?client-id=xxxxx&enable-funding=venmo&currency=GBP"
  data-sdk-integration-source="button-factory"
></script>
```


It expects the following JS content to be present:

```
<script>
  var ticketTypes = [
    {
      name: "adult",
      description: "Adult member/guest",
      headCount: 1,
      price: 15,
    },
    {
      name: "family",
      description: "Family (2 adults, 2 children)",
      headCount: 4,
      price: 42,
    },
  ];
  var mealTypes = [
    {
      name: "noPref",
      description: "No preference",
    },
    {
      name: "other",
      description: "Other (please specify)",
      hasOther: true,
    },
  ];
</script>
```
 *
 */
class PaypalTickets {
  constructor() {
    // HTML elements
    this.els = {
      container: null,
      name: null,
      tickets: null,
      ticketSelects: [],
      meals: null,
      mealsSelects: [],
      mealsOther: null,
      order: null,
      orderTotal: null,
      submit: null,
    };

    // CONST values used by Paypal
    this.ORDER_TITLE = "PHX-Tickets";
    this.ORDER_SHIPPING = 0;
    this.ORDER_TAX = 0;

    // order values
    this.orderTotalValue = 0;
    this.orderTicketCount = 0;
    this.orderHeadCount = 0;
    this.orderMealCount = 0;
    this.orderDescription = "";
    this.orderSummary = "";

    this.selectedTickets = [];
    this.selectedMeals = [];

    // import global (window) variables
    this.paypal = window.paypal;
    this.ticketTypes = window.ticketTypes || [];
    this.mealTypes = window.mealTypes || [];
  }

  init() {
    this.els.container = document.querySelector(".PaypalTickets");
    if (!this.els.container) return false;

    this.addInitialHTML();
    this.selectElements();
    this.addListeners();
    this.addTicketContent();
    this.addMealContent();
    this.initPaypal();
    this.updateOrder();
  }

  /**
   * Quick hacky way to insert the initial HTML template
   */
  addInitialHTML() {
    const template = `
      <div class="PaypalTickets-orderDetails">
        <div class="Editorial">
          <h3>Your order</h3>
        </div>
        <div class="Form">
          <div class="Form-row">
            <label class="Form-label" for="contact-details">Full name:</label>
            <input
              type="text"
              name="contact-details"
              class="Form-input--text Form-input--inline PaypalTickets-input--name"
            />
          </div>
        </div>
      </div>
      <div class="PaypalTickets-tickets Form">
        <h3 class="PaypalTickets-title">Ticket types</h3>
      </div>
      <div class="PaypalTickets-meals Form">
        <h3 class="PaypalTickets-title">Meal types</h3>
      </div>
      <div class="PaypalTickets-order u-hidden">
        <div class="Editorial">
          <h3>Order summary</h3>
          <p class="PaypalTickets-orderTotal"></p>
        </div>
      </div>
      <div class="PaypalTickets-submit u-hidden"></div>
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
    this.els.name = c.querySelector(".PaypalTickets-input--name");
    this.els.tickets = c.querySelector(".PaypalTickets-tickets");
    this.els.meals = c.querySelector(".PaypalTickets-meals");
    this.els.order = c.querySelector(".PaypalTickets-order");
    this.els.orderTotal = c.querySelector(".PaypalTickets-orderTotal");
    this.els.submit = c.querySelector(".PaypalTickets-submit");
  }

  /**
   * Add triggers to fire on input change
   */
  addListeners() {
    this.els.name.addEventListener("input", this.updateOrder.bind(this));
  }

  /**
   * Add dynamic ticket content
   */
  addTicketContent() {
    this.ticketTypes.forEach((ticketType) => {
      const ticketTypeDivEl = document.createElement("div");
      ticketTypeDivEl.classList.add(
        "PaypalTickets-ticketType",
        `PaypalTickets-ticketType--${ticketType.name}`
      );
      this.els.tickets.appendChild(ticketTypeDivEl);

      const ticketTypeSelectWrapEl = document.createElement("div");
      ticketTypeSelectWrapEl.classList.add(
        "PaypalTickets-selectWrap",
        "Form-selectWrap",
        "Form-selectWrap--inline"
      );
      ticketTypeDivEl.appendChild(ticketTypeSelectWrapEl);

      const ticketTypeSelectEl = document.createElement("select");
      ticketTypeSelectEl.name = ticketType.name;
      ticketTypeSelectEl.dataset.price = ticketType.price;
      ticketTypeSelectEl.dataset.headCount = ticketType.headCount;
      ticketTypeSelectEl.classList.add("Form-select");
      ticketTypeSelectEl.addEventListener("input", this.updateOrder.bind(this));
      ticketTypeSelectWrapEl.appendChild(ticketTypeSelectEl);
      this.els.ticketSelects.push(ticketTypeSelectEl);

      for (let counter = 0; counter <= 5; counter++) {
        const optionEl = document.createElement("option");
        optionEl.textContent = counter;
        ticketTypeSelectEl.appendChild(optionEl);
      }

      const labelEl = document.createElement("label");
      labelEl.classList.add("PaypalTickets-label");
      labelEl.textContent = `${ticketType.description} (£${ticketType.price})`;
      ticketTypeDivEl.appendChild(labelEl);
    });
  }

  /**
   * Add dynamic meal content
   */
  addMealContent() {
    this.mealTypes.forEach((mealType) => {
      const mealTypeDivEl = document.createElement("div");
      mealTypeDivEl.classList.add(
        "PaypalTickets-mealType",
        `PaypalTickets-mealType--${mealType.name}`
      );
      this.els.meals.appendChild(mealTypeDivEl);

      const mealTypeSelectWrapEl = document.createElement("div");
      mealTypeSelectWrapEl.classList.add(
        "PaypalTickets-selectWrap",
        "Form-selectWrap",
        "Form-selectWrap--inline"
      );
      mealTypeDivEl.appendChild(mealTypeSelectWrapEl);

      const mealTypeSelectEl = document.createElement("select");
      mealTypeSelectEl.name = mealType.name;
      mealTypeSelectEl.classList.add("Form-select");
      mealTypeSelectEl.addEventListener("change", this.updateOrder.bind(this));
      mealTypeSelectWrapEl.appendChild(mealTypeSelectEl);
      this.els.mealsSelects.push(mealTypeSelectEl);

      for (let counter = 0; counter <= 5; counter++) {
        const optionEl = document.createElement("option");
        optionEl.textContent = counter;
        mealTypeSelectEl.appendChild(optionEl);
      }

      const labelEl = document.createElement("label");
      labelEl.classList.add("PaypalTickets-label");
      labelEl.textContent = mealType.description;
      mealTypeDivEl.appendChild(labelEl);

      if (mealType.hasOther) {
        const mealTypeOtherInputEl = document.createElement("input");
        mealTypeOtherInputEl.type = "text";
        mealTypeOtherInputEl.classList.add(
          "Form-input--text",
          "Form-input--inline"
        );
        mealTypeOtherInputEl.addEventListener(
          "change",
          this.updateOrder.bind(this)
        );
        mealTypeDivEl.appendChild(mealTypeOtherInputEl);
        this.els.mealsOther = mealTypeOtherInputEl;
      }
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
          color: "gold",
          layout: "vertical",
          label: "buynow",
        },
        createOrder: (data, actions) => {
          return actions.order.create({
            purchase_units: [
              {
                description: this.orderDescription,
                custom: this.orderDescription,
                cn: this.orderDescription,
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
                items: [
                  {
                    name: this.orderSummary,
                    unit_amount: {
                      currency_code: "GBP",
                      value: this.orderTotalValue,
                    },
                    quantity: 1,
                    custom: this.orderDescription,
                    cn: this.orderDescription,
                  },
                ],
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
      .render(".PaypalTickets-submit");
  }

  /**
   * Recheck the order every time something is updated
   */
  updateOrder() {
    this.updateOrderTickets();
    this.updateOrderMeals();
    this.updateOrderDescription();
    this.updateOrderValidity();
  }

  /**
   * Count ticket orders
   */
  updateOrderTickets() {
    this.orderTotalValue = 0;
    this.orderTicketCount = 0;
    this.orderHeadCount = 0;
    this.selectedTickets = [];

    this.els.ticketSelects.forEach((ticketSelectEl) => {
      const selectedValue = parseInt(
        ticketSelectEl.options[ticketSelectEl.selectedIndex].value,
        10
      );
      if (selectedValue > 0) {
        this.orderTotalValue += selectedValue * ticketSelectEl.dataset.price;
        this.orderTicketCount += selectedValue;
        this.orderHeadCount += selectedValue * ticketSelectEl.dataset.headCount;
        this.selectedTickets.push({
          name: ticketSelectEl.name,
          ticketCount: selectedValue,
          headCount: ticketSelectEl.dataset.headCount,
          price: ticketSelectEl.dataset.price,
        });
      }
    });
  }

  /**
   * Count meal orders
   */
  updateOrderMeals() {
    this.orderMealCount = 0;
    this.selectedMeals = [];

    this.els.mealsSelects.forEach((mealsSelect) => {
      const selectedValue = parseInt(
        mealsSelect.options[mealsSelect.selectedIndex].value,
        10
      );
      if (selectedValue > 0) {
        this.orderMealCount += selectedValue;
        this.selectedMeals.push({
          name: mealsSelect.name,
          mealCount: selectedValue,
        });
      }
    });
  }

  /**
   * Update order description sentences
   */
  updateOrderDescription() {
    this.orderDescription = `${this.ORDER_TITLE},${this.els.name.value},`;
    this.orderSummary = "(";

    this.selectedTickets.forEach((ticket) => {
      this.orderDescription += `${ticket.name},${ticket.ticketCount},`;
      this.orderSummary += `${ticket.name} ${ticket.ticketCount}, `;
    });

    this.selectedMeals.forEach((meal) => {
      this.orderDescription += `${meal.name},${meal.mealCount},`;
      this.orderSummary += `${meal.name} ${meal.mealCount}, `;
    });

    this.orderDescription += `otherDetails,${this.els.mealsOther.value},`;
    this.orderDescription += `GBP,${this.orderTotalValue}`;
    this.orderSummary = this.orderSummary.slice(0, -2) + ")";
  }

  /**
   * Check if the order is valid before displaying paypal button
   */
  updateOrderValidity() {
    // if there are orders, show order summary
    if (this.orderTotalValue > 0) {
      this.els.orderTotal.textContent = `£${this.orderTotalValue}`;
      this.els.order.classList.remove("u-hidden");
    } else {
      this.els.order.classList.add("u-hidden");
    }

    if (this.orderMealCount > this.orderHeadCount) {
      this.els.orderTotal.textContent =
        "Please check your selection, there are more dietary requirements than people.";
    }

    // if the user has entered all required info, and if there aren't more meal
    // orders than tickets (heads), show paypal
    if (
      this.els.name.value.length >= 2 &&
      this.orderTotalValue > 0 &&
      this.orderMealCount <= this.orderHeadCount
    ) {
      this.els.submit.classList.remove("u-hidden");
    } else {
      this.els.submit.classList.add("u-hidden");
    }
  }
}

const paypalTickets = new PaypalTickets();

export default paypalTickets;
