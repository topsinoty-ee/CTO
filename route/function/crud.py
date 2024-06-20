from api.airtable_ops import (
    init_table,
    search_record_by_id,
)
from flask_login import current_user
from flask import (redirect, render_template, request, flash)
from api.logging_config import logger
from api.utils import convert_to_json, CRUD


def edit(table, id):
    displayed_data = []
    record = search_record_by_id(table, id)
    logger.info(record)
    if request.method == 'POST':
        form_data = request.form['form_data']

        if form_data is not None:
            logger.info(f"form_data: {form_data}")
            displayed_data = convert_to_json(form_data)
        # Process the displayed_data as needed
        logger.info(f"Edited data: {displayed_data}")
        return render_template('update_form.html',
                               formdata=displayed_data,
                               data=record,
                               table=table)

    return render_template('update_form.html',
                           formdata=displayed_data,
                           is_edit=True)


def add(table: str):
    displayed_data = []

    if request.method == 'POST':
        form_data = request.form['form_data']
        computed_field = request.form['computed_field']

        if form_data is not None:
            logger.info(f"form_data: {form_data}")
            displayed_data = convert_to_json(form_data)
            displayed_data = [
                field for field in displayed_data if field['editable']
            ]

            logger.info(f"Data to add: {displayed_data}")
            return render_template('add_form.html',
                                   formdata=displayed_data,
                                   table=table,
                                   computed_field=computed_field)

    return render_template('add_form.html',
                           formdata=displayed_data,
                           table=table)


def delete(table, item_id):
    """
    Delete an item from the specified table.

    Args:
        table (str): The table from which to delete the item.
        item_id (str): The ID of the item to delete.

    Returns:
        str: Redirect to the applications page after deletion.
    """
    Table = init_table(table)
    CRUD(Table, item_id, option='delete')
    flash('Item deleted successfully', 'success')
    return redirect(f'/{current_user.id}/company-dashboard')


def update(table_key: str, id):
    try:
        Table = init_table(table_key)
        record = search_record_by_id(Table, id)
        logger.info(record)
        # write logic that compare
        data = {
            key: value
            for key, value in request.form.items() if value.strip() != ""
        }
        data.pop('id', None)
        files = request.files.to_dict()

        logger.info(f"data: {data}")
        logger.info(f"files: {files}")

        CRUD(Table, record_id=id, data=data, files=files, option='update')
        return redirect(f'/{current_user.id}/company-dashboard')
    except Exception as e:
        logger.error(
            f"Error updating record with ID {id} in table {table_key}: {e}")
        return "An error occurred", 500


def create(table: str):
    try:
        Table = init_table(table)

        # Get form data and log it
        formdata = request.form.items()
        computed_field = request.form.get('computed_field')
        logger.info(f"computed_field: {computed_field}")
        logger.info(f"formdata: {formdata}")

        # Parse the computed_field JSON string into a Python dictionary
        computed_field_data = convert_to_json(computed_field)
        logger.info(f"computed_field_data: {computed_field_data}")

        # Add form data to the data dictionary, excluding the computed field initially
        data = {
            key: value
            for key, value in formdata if key != 'computed_field'
        }
        logger.info(f"data: {data}")
        # Add the computed field to the data dictionary
        if 'key' in computed_field_data and 'value' in computed_field_data:
            data[computed_field_data['key']] = [computed_field_data['value']]
        logger.info(f"data after adding computed_field: {data}")

        # Get files and log them
        files = request.files.to_dict()
        logger.info(f'files: {files}')

        # Use CRUD function to create the record
        CRUD(Table, data=data, files=files, option='create')

        # Redirect to the company dashboard
        return redirect(f'/{current_user.id}/company-dashboard')

    except Exception as e:
        logger.error(f"Error adding record to table {table}: {e}")
        return "An error occurred", 500
