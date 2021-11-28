from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from splitwise import serializers, models


class UserProfileApiView(APIView):
    """Test API View"""
    serializer_class = serializers.UserProfileSerializer

    def post(self, request) -> Response:
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            name = serializer.validated_data.get('name')
            return Response({'message': f'User {name} created successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateGroupApiView(APIView):
    """Group Creation View"""
    serializer_class = serializers.GroupSerializer

    def post(self, request) -> Response:
        """ Create a hello message with our name """

        all_users = []
        for user_email in request.data.get('members', []):
            all_users.append(models.UserProfile.objects.get(email=user_email).id)
        request.data['members'] = all_users
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'Group {serializer.data.get("group_name")} Created successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddUserToGroupApiView(APIView):
    """Add member to existing group Creation View"""

    def post(self, request) -> Response:
        """ Create a hello message with our name """
        group_name = request.data.get('group_name')
        user_email = request.data.get('user_email')
        user = models.UserProfile.objects.get(email=user_email)
        group = models.Group.objects.get(group_name=group_name)
        if user not in group.members.all():
            group.members.add(user.id)
            return Response({'message': f'User {user_email} successfully added to group {group.group_name}'})
        return Response({'message': 'User already exists in the group'}, status=status.HTTP_400_BAD_REQUEST)


class ShowGroupMembersApiView(APIView):
    """Show group members"""

    def get(self, request) -> Response:
        """ Create a hello message with our name """
        group_name = request.GET['name']
        try:
            group = models.Group.objects.get(group_name=group_name)
            # all_members = [x.name for x in group.members]
            all_members = [str(x) for x in group.members.all()]
            return Response({'message': f'{all_members}'})
        except models.Group.DoesNotExist:
            return Response(
                {'message': 'Group Does not exist !'
                 },
                status=status.HTTP_404_NOT_FOUND
            )


class ShowUserDetailsApiView(APIView):
    """Show user details"""

    def get(self, request) -> Response:
        user_email = request.GET['email']
        try:
            user = models.UserProfile.objects.get(email=user_email)
            f_debts = models.Debt.objects.filter(from_user=user)
            t_debts = models.Debt.objects.filter(to_user=user)
            debt_data = dict()
            debit = 0
            credit = 0
            for i in f_debts:
                debt_data[i.to_user.name] = debt_data.get(i.to_user.name, 0) - i.amount
                debit -= i.amount
            for i in t_debts:
                debt_data[i.from_user.name] = debt_data.get(i.from_user.name, 0) + i.amount
                credit += i.amount
            return Response(
                {'message':
                    {
                        'user': f'{user}',
                        'debit': debit,
                        'credit': credit,
                        'data': [f'User {user.name} ows {debt_data[x]} to user {x}' if debt_data[
                                                                                           x] > 0 else f'User {user.name} owes {-1 * debt_data[x]} to {x}'
                                 for x in debt_data if
                                 x != user.name and debt_data[x] != 0],
                    }
                }
            )
        except models.UserProfile.DoesNotExist:
            return Response(
                {'message': 'User Does not exist !'
                 },
                status=status.HTTP_404_NOT_FOUND
            )


class CreateExpenseApiView(APIView):
    """Group Creation View"""
    serializer_class = serializers.ExpenseSerializer

    def post(self, request) -> Response:
        description = request.data.get('description')
        all_users = request.data.get('users')
        all_users = models.UserProfile.objects.filter(email__in=all_users)
        paid_by = request.data.get('paid_by')
        paid_by_user = models.UserProfile.objects.filter(email=paid_by).first()
        amount = request.data.get('amount')
        group_name = request.data.get('group_name', None)
        expense_name = request.data.get('name')
        if models.Expense.objects.filter(name=expense_name).count() > 0:
            return Response({
                "message": "Expense name should be unique"
            }, status=status.HTTP_400_BAD_REQUEST)
        group = None
        if group_name is not None:
            group = models.Group.objects.get(group_name=group_name)
        per_member_share = amount / len(all_users)
        expense_users = []
        repayments = []
        for user in all_users:
            if user != paid_by_user:
                debt = models.Debt.objects.create(**{"from_user": paid_by_user,
                                                     "to_user": user,
                                                     "amount": per_member_share})
                repayments.append(debt)
            expense_user_dict = {"user": user,
                                 "paid_share": 0 if user != paid_by_user else per_member_share,
                                 "owed_share": per_member_share,
                                 "net_balance": -per_member_share if user != paid_by_user else amount - per_member_share
                                 }
            expense_user = models.ExpenseUser.objects.create(**expense_user_dict)
            expense_users.append(expense_user)
        # now create expense
        expense = {
            'expense_group': group,
            'description': description,
            'amount': amount,
            'name': expense_name
        }
        expense = models.Expense.objects.create(**expense)
        expense.repayments.set(repayments)
        expense.users.set(expense_users)
        expense.save()
        return Response({'message': 'Expense Created successfully'})


class ShowGroupDetailsApiView(APIView):
    def get(self, request) -> Response:
        group_name = request.GET['name']
        try:
            group = models.Group.objects.get(group_name=group_name)
            expenses = models.Expense.objects.filter(expense_group=group, payment=False)
            data = list()
            for expense in expenses:
                exp = {
                    "name": expense.name,
                    "Description": expense.description,
                    "repayments": [str(x) for x in expense.repayments.all() if
                                   x.from_user != x.to_user and x.amount != 0]
                }
                data.append(exp)
            return Response(
                {'message': data
                 }
            )
        except models.Group.DoesNotExist:
            return Response(
                {'message': 'Group Does not exist !'
                 },
                status=status.HTTP_404_NOT_FOUND
            )


class DeleteUserApiView(APIView):
    def delete(self, request) -> Response:
        user_email = request.GET['email']
        try:
            user = models.UserProfile.objects.get(email=user_email)
            if user:
                user.delete()
                return Response(
                    {'message': 'User deleted'
                     }
                )
        except models.UserProfile.DoesNotExist:
            return Response({
                "message": "User does not exist"
            })


class DeleteGroupApiView(APIView):
    def delete(self, request) -> Response:
        group_name = request.GET['name']
        try:
            group = models.Group.objects.get(group_name=group_name)
            if group:
                group.delete()
                return Response(
                    {
                        'message': 'Group deleted'
                    }
                )
        except models.Group.DoesNotExist:
            return Response({
                "message": "Group does not exist"
            })


class RecordPaymentApiView(APIView):
    def post(self, request) -> Response:
        from_user_email = request.data.get('from_user')
        to_user_email = request.data.get('to_user')
        amount = request.data.get('amount')
        group_name = request.data.get('group_name')
        expense_name = request.data.get('expense_name')
        from_user = models.UserProfile.objects.get(email=from_user_email)
        to_user = models.UserProfile.objects.get(email=to_user_email)
        try:
            if group_name is None:

                models.Debt.objects.create(**{
                    "from_user": from_user,
                    "to_user": to_user,
                    "amount": amount
                })
                return Response({
                    "message": "Payment recorded successfully"
                })
            else:
                expense = models.Expense.objects.get(name=expense_name)
                if expense.expense_group != models.Group.objects.get(group_name=group_name):
                    return Response({
                        "message": "Expense  not in group, please check !"
                    }, status=status.HTTP_400_BAD_REQUEST)
                flag = False
                for i in expense.repayments.all():
                    if i.from_user == to_user and i.to_user == from_user:
                        flag = True
                        i.amount = i.amount - amount
                        i.save()
                        break
                if not flag:
                    debt = models.Debt.objects.create(**{
                        "from_user": to_user,
                        "to_user": from_user,
                        "amount": amount
                    })
                    expense.repayments.add(debt)
                expense.save()
                flag = False
                for i in expense.repayments.all():
                    if i.amount > 0:
                        flag = True
                        break
                if not flag:
                    expense.payment = True
                    expense.save()
                return Response({
                    "message": "Expense Payment recorded successfully"
                })
        except models.UserProfile.DoesNotExist:
            return Response({
                "message": "User does not exist"
            })
        except models.Expense.DoesNotExist:
            return Response({
                "message": "Expense does not exist"
            })
