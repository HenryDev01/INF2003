
$(document).on('click', '.edit-review-btn', function(e) {
  e.preventDefault();
  // Fill the modal inputs with data from the clicked review
  $('#review_id').val($(this).data('review-id'));
  $('#review_title').val($(this).data('title'));
  $('#review_text').val($(this).data('text'));

  // Set rating radio buttons
  let rating = $(this).data('rating');
  $(`#star${rating}`).prop('checked', true);

  // Change modal title to 'Edit Review'
  $('#reviewModalLabel').text('Edit Review');

  // Show the modal
  $('#reviewModal').modal('show');
});
$(document).on('click','.write-review-btn',function(e)
{
      $('#reviewModal').modal('show');

});
// on close reset modal
$('#reviewModal').on('hidden.bs.modal', function () {
  $('#reviewForm')[0].reset();
  $('#reviewModalLabel').text('Write Review');
  $('#review_id').val("");
});

$("#reviewForm").on("submit", function (e) {
    e.preventDefault();
    let review_id, url;
    review_id = $("#review_id").val();
    const formData = {
      rating: $("input[name='rating']:checked").val(),
      review_title: $("#review_title").val(),
      review_message: $("#review_text").val()
    };
    if(review_id)
    {
        url = "/review/edit/" + review_id
        formData.review_id = review_id
    }else
    {
         const product_id =  $("#product_id").val();
         url = "/create_review/" + product_id
    }



    $.ajax({
      url: url,
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(formData),
      dataType:'json',
      success: function (response) {
            location.reload();
      },
      error: function (xhr) {
         const response = xhr.responseJSON;
        const message = response && response.message ? response.message : "An error occurred.";
        alert(message);
      }
    });
});



// delete
$('.delete-review').click(function(e) {
    e.preventDefault();
    if(!confirm('Are you sure you want to delete this review?')) return;

    let reviewId = $(this).data('review-id');
    let url = "/review/delete/" + reviewId
    $.ajax({
      url: url,
      type: 'DELETE',
      success: function(data) {

          location.reload();

      },
      error: function() {
        alert('Error deleting review');
      }
});
});

document.querySelectorAll('.product-thumb-img').forEach(thumb => {
  thumb.addEventListener('click', function() {
    const mainImg = document.querySelector('.main-product-img');
    mainImg.src = this.src;
  });
});



document.getElementById('updateBtn').addEventListener('click', function() {
  submitCartAction('update');
});

document.getElementById('deleteBtn').addEventListener('click', function() {
  submitCartAction('delete');
});

document.getElementById('checkoutBtn').addEventListener('click', function() {
  submitCartAction('checkout');
});


  function submitCartAction(action) {
    let form = $('#bulkCartForm');
    let formData = form.serializeArray(); // serialize all inputs
    formData.push({name: 'action', value: action}); // add action manually
    $.ajax({
      url: form.attr('action'),
      method: 'POST',
      data: $.param(formData),  // turn array back into query string
      success: function(response) {

        if (response.success) {
            if(action == "checkout")
                window.location.href = "/checkout";
            else
                location.reload(); // or update the cart UI dynamically
        } else {
          alert('Failed: ' + (response.error || 'Unknown error'));
        }
      },
      error: function() {
        alert('An error occurred.');
      }
    });
  }



$("#checkoutForm").on("submit", function (e) {
    e.preventDefault();

    $.ajax({
        url: "/customer_add_order",
        type: "POST",
        data: $(this).serialize(),
        success: function (response) {
            console.log("Order placed successfully!");
            alert("Order placed!");
            window.location.href = "/customer_order/all";
            location.refresh();
        },
        error: function (xhr, status, error) {
            console.error("Error placing order:", error);
            alert("Something went wrong!");
        }
    });
});
